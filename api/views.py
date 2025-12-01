from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from . import utils


class CheckApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        data = {
            "status": "ok",
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


# -------------------- START TEAM -------------------- #
class TeamInfoApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        try:
            team_info = utils.get_team_info()
            return Response(
                data={"status": "ok", "team_info": team_info},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class TeamMatchesApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            team_matches = utils.get_team_matches()
            return Response(
                data={"status": "ok", "team_matches": team_matches},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
# -------------------- END TEAM -------------------- #


# -------------------- START PLAYER -------------------- #
class SearchPlayerApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            name = request.data.get("name")
            if not name:
                return Response(
                    data={"error": "name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player = utils.search_player(name=name)
            return Response(
                data={"status": "ok", "player": player},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class PlayerProfileApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            id = request.data.get("id")
            name = request.data.get("name")
            if not id or not name:
                return Response(
                    data={"error": "name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player_profile = utils.get_player_profile(id=id, player_name=name)
            return Response(
                data={"status": "ok", "player_profile": player_profile},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class PlayerStatApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            id = request.data.get("id")
            name = request.data.get("name")
            if not id or not name:
                return Response(
                    data={"error": "name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player_stat = utils.get_player_stats_overview(id=id, player_name=name)
            return Response(
                data={"status": "ok", "player_stat": player_stat},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
# -------------------- START PLAYER -------------------- #


# -------------------- START MATCHES -------------------- #
class GetUpcomingMatchesApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            upcoming_matches = utils.get_upcoming_matches()
            return Response(
                data={"status": "ok", "upcoming_matches": upcoming_matches},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class GetMatchDetailsApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            id = request.data.get("id")
            match_name = request.data.get("match_name")
            if not id or not match_name:
                return Response(
                    data={"error": "match_name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            match_details = utils.get_match_details(id=id, match_name=match_name)
            return Response(
                data={"status": "ok", "match_details": match_details},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
# -------------------- START MATCHES -------------------- #
