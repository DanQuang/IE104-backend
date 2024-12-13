from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CreditAccount, Tier

class UserProfileView(APIView):
    # Enforce authentication
    permission_classes = [IsAuthenticated]  # Only need IsAuthenticated

    def get(self, request):
        try:
            # Get the logged-in user
            user = request.user

            # Get the first credit account of the logged-in user (assuming only one account per user)
            credit_account = user.credit_accounts.first()  # Get the first credit account
            credit_account_data = None
            if credit_account:
                credit_account_data = {
                    'account_name': credit_account.account_name,
                    'account_number': credit_account.account_number,
                }

            # Get the user's current tier (assuming only one active tier per user)
            tier = user.tiers.first()  # Get the first tier
            tier_data = None
            if tier:
                tier_data = {
                    'current_tier': tier.current_tier,
                    'service': tier.service.description,
                    'start_day': tier.start_day,
                    'end_day': tier.end_day,
                }

            # Serialize user data
            user_data = {
                'email': user.email,
                'full_name': user.full_name,
                'credit_account': credit_account_data,
                'tier': tier_data,
            }

            return Response(user_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
