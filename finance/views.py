from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, BonusRequest,Notification
from .serializers import UserSerializer, BonusRequestSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.generic import TemplateView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class BonusRequestViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'MANAGER':
            return BonusRequest.objects.filter(created_by=user)
        elif user.role == 'FINANCE':
            return BonusRequest.objects.all()
        return BonusRequest.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        if self.request.user.role != 'MANAGER':
            raise PermissionError('Only managers can create bonus requests')
        bonus_request = serializer.save(
            created_by=self.request.user,
            attachment=self.request.FILES.get('attachment')
        )
        # Send notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{bonus_request.assigned_to.id}",
            {
                "type": "notification",
                "message": f"New bonus request assigned to you by {self.request.user.username}",
                "bonus_id": bonus_request.id,
                "notification_type": "NEW_REQUEST"
            }
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            bonus_request = self.get_object()
            if request.user.role != 'FINANCE':
                return Response(
                    {'error': 'Only finance staff can approve requests'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            action_type = request.data.get('action', 'APPROVED')
            if action_type not in ['APPROVED', 'REJECTED']:
                return Response(
                    {'error': 'Invalid action type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            bonus_request.status = action_type
            bonus_request.save()
            # Create notification message first
            notification_message = f"Your bonus request has been {action_type.lower()}"

            # Create notification object
            notification = Notification.objects.create(
            user=bonus_request.created_by,
            message=notification_message,
            bonus_request=bonus_request
        )

            # Send notification
            channel_layer = get_channel_layer()
            # notification_message = f"Your bonus request has been {action_type.lower()}"

            async_to_sync(channel_layer.group_send)(
                f"user_{bonus_request.created_by.id}",
                {
                    "type": "notification",
                    "message": notification_message,
                    "bonus_request_id": bonus_request.id,
                    "notification_id": notification.id,
                    "created_at": notification.created_at.isoformat()
                }
            )

            # Notify assigned user if different from creator
                # Notify assigned user if different from creator
            if bonus_request.assigned_to.id != bonus_request.created_by.id:
                assigned_notification = Notification.objects.create(
                    user=bonus_request.assigned_to,
                    message=f"Bonus request from {bonus_request.created_by.username} has been {action_type.lower()}",
                    bonus_request=bonus_request
                )
                async_to_sync(channel_layer.group_send)(
                    f"user_{bonus_request.assigned_to.id}",
                    {
                        "type": "notification",
                        "message": assigned_notification.message,
                        "bonus_id": bonus_request.id,
                        "notification_id": assigned_notification.id,
                        "created_at": assigned_notification.created_at.isoformat()
                    }
                )

            # Create notification in database
           
            return Response({
                'status': action_type.lower(),
                'bonus_id': bonus_request.id,
                'message': f'Bonus request has been {action_type.lower()}'
            })
        except BonusRequest.DoesNotExist:
            return Response(
                {'error': 'Bonus request not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


