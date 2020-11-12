from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PartcipantsSerializer
from rest_framework import status
from .models import Participants, Winners
from django.core.exceptions import ObjectDoesNotExist
from .tasks import send_email_w_celery


def create_password(request):
    return render(request, "toilet_paper_giveaway/create_password.html", {})


@api_view(["POST"])
def register_participant(request):

    if request.method == "POST":
        request_data = request.data
        email = request_data["email"]
        # Validate if email exist, before continue
        email_exist = validate_email(email)
        if email_exist:
            # Resend email
            send_email(email)
            return Response(
                dict(message="Participant already exist, email has been re-sent"),
                status=status.HTTP_202_ACCEPTED,
            )

        serializer = PartcipantsSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            # Once saved, send email
            send_email(email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
def get_winner(request):

    if request.method == "GET":
        # Not the best in performance, but for this test example, is the fastest way
        winner = Participants.objects.order_by("?").first()
        to_response = PartcipantsSerializer(winner).data
        to_response.update(message="Congratulations you won!")

        # Saving Winner on database.
        winner_to_save = Winners()
        winner_to_save.participant_id = winner
        winner_to_save.save()

        return Response(to_response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def update_participant_password(request):
    if request.method == "POST":
        data = request.data
        participant_id = data["participant_id"]
        password = data["password"]
        Participants.objects.filter(id=participant_id).update(password=password)
        to_response = dict(message="Password created successfully", success=True)
        return Response(to_response, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def validate_email(email: str) -> bool:
    """
    Method validates if received email already exist on database

    :param email: Email of participant to validate existence on database
    :type email: str
    :return: True or False if email already exist
    :rtype: bool
    """
    try:
        participant = Participants.objects.get(email=email)
    except ObjectDoesNotExist:
        print("Participant does not exist")
        return False

    return True


def send_email(email):
    participant = Participants.objects.get(email=email)
    name = participant.name
    last_name = participant.last_name
    participant_id = participant.id
    send_email_w_celery.delay(name, last_name, email, participant_id)
    return True
