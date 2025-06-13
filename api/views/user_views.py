from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.user_service import UserService
from django.contrib.auth import get_user_model
from ..models import UserBranch
CustomUser = get_user_model()
from rest_framework.permissions import IsAuthenticated
class CreateUserView(generics.CreateAPIView):
    """
    API View to create a user and assign them to multiple branches.
    """

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_data = UserService.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
                user_code=data.get("user_code"),
                mobile=data.get("mobile"),
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                branch_ids=data.get("branch_ids", [])  # ✅ Accept multiple branches as a list
            )

            return Response(
                {
                    "message": "User created successfully",
                    "user": user_data  # ✅ Directly return user dictionary
                },
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(generics.UpdateAPIView):
    """
    API View to update a user's details.
    """

    def put(self, request, user_id):
        try:
            data = request.data
            user = UserService.update_user(
                user_id=user_id,
                username=data.get("username"),
                email=data.get("email"),
                user_code=data.get("user_code"),
                mobile=data.get("mobile"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                branch_ids=data.get("branch_ids", [])
            )

            return Response(
                {
                    "message": "User updated successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "user_code": user.user_code,
                        "mobile": user.mobile,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "branches_assigned": [ub.branch.id for ub in user.user_branches.all()]
                    }
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API View to get all user-branch assignments.
    """
    def get(self, request):
            # ✅ Check if the user is a superuser
            if not request.user.is_superuser:
                return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

            users = CustomUser.objects.all()

            user_list = []
            for user in users:
                # ✅ Get all branches assigned to the user
                branches = UserBranch.objects.filter(user_id=user.id).select_related("branch")

                branch_details = [
                    {
                        "id": ub.branch.id,
                        "branch_name": ub.branch.branch_name,  # Change if needed
                    }
                    for ub in branches
                ]

                user_list.append({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "branches": branch_details,  # ✅ Add branch list
                })

            return Response(user_list, status=status.HTTP_200_OK)

class GetSingleUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        # ✅ Check if the user is a superuser
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        user = CustomUser.objects.get(id=user_id)

        branches = UserBranch.objects.filter(user_id=user.id).select_related("branch")

        branch_details = [
            {
                "id": ub.branch.id,
                "branch_name": ub.branch.branch_name,  # Change if needed
            }
            for ub in branches
        ]

        return Response({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile": user.mobile,
            "email": user.email,
            "user_code": user.user_code,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "branches": branch_details
        })
    