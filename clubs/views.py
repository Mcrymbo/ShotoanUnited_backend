from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import RegistrationToken, Dojo, Coach, Player
from datetime import datetime
from django.conf import settings

class GenerateRegistrationLinkAPIView(APIView):
    def post(self, request):
        user_type = request.data.get("user_type")
        dojo_id = request.data.get("dojo_id")  # Optional, for players
        dojo = None
        
        if user_type not in ["coach", "player"]:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_type == "player" and dojo_id:
            try:
                dojo = Dojo.objects.get(id=dojo_id)
            except Dojo.DoesNotExist:
                return Response({"error": "Invalid dojo ID"}, status=status.HTTP_404_NOT_FOUND)
        
        token = RegistrationToken.objects.create(user_type=user_type, dojo=dojo)
        link = f"{settings.DOMAIN}/register/{token.token}/"
        
        # Send link via WhatsApp/SMS or return it
        # Example: send_sms_or_whatsapp(phone_number, link)
        
        return Response({"link": link}, status=status.HTTP_201_CREATED)
    

class RegisterAPIView(APIView):
    def post(self, request, token):
        try:
            reg_token = RegistrationToken.objects.select_related('dojo').get(
                token=token, is_used=False, # expiration_time__gt=datetime.now()
            )
        except RegistrationToken.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        belt_rank = request.data.get("belt_rank", "")  # Default to empty if not provided

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
            validate_password(password)
        except ValidationError as e:
            return Response({"error": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if reg_token.user_type == "coach":
                Coach.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    certifications=request.data.get("certifications", ""),  # Only pass certifications for coach
                )
            elif reg_token.user_type == "player":
                dojo = reg_token.dojo
                if not dojo:
                    return Response({"error": "No dojo associated with this registration token"}, status=status.HTTP_400_BAD_REQUEST)
                Player.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    belt_rank=belt_rank,  # Ensure belt_rank is passed
                    dojo=dojo,
                )

            reg_token.is_used = True
            reg_token.save()
            return Response({"message": f"{reg_token.user_type.capitalize()} registration successful"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Registration failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
