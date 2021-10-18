from django.http import HttpResponse
from supertokens_python.recipe.session.framework.django.syncio import verify_session

from supertokens_python.recipe.session.syncio import create_new_session


def create(request):
    session = create_new_session(request, 'user_id')
    return HttpResponse("new session access token = " +
                        session.get_access_token())


@verify_session(session_required=False)
def user(request):
    return HttpResponse("new session access token = " +
                        request.state.get_user_id())
