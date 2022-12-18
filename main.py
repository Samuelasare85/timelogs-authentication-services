from prisma import Prisma
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType
from ariadne import load_schema_from_path, MutationType, make_executable_schema, QueryType, ScalarType
from src.resolvers import user_resolvers
from ariadne.contrib.federation import make_federated_schema

schema = load_schema_from_path('schema.graphql')
 
query = QueryType()
mutation = MutationType()
user = FederatedObjectType("User")
datetime = ScalarType("DateTime")

prisma = Prisma()

query.set_field("me", user_resolvers.resolve_me)
query.set_field("user", user_resolvers.resolve_user)
query.set_field("allUsers", user_resolvers.resolve_all_users)
query.set_field("activeUsers", user_resolvers.resolve_active_users)
query.set_field("inActiveUsers", user_resolvers.resolve_inactive_users)
query.set_field("getUsersByDepartment", user_resolvers.resolve_get_users_by_department)
mutation.set_field("createUser", user_resolvers.resolve_create_user)
mutation.set_field("loginUser", user_resolvers.resolve_login_user)
mutation.set_field("logoutUser", user_resolvers.resolve_logout_user)
mutation.set_field("updateUser", user_resolvers.resolve_update_user)
mutation.set_field("deleteUser", user_resolvers.resolve_delete_user)

@datetime.serializer
def serialize_datetime(value):
    return value.isoformat()

@user.reference_resolver
async def resolve_user_reference(_, info, id):
    try:
        await prisma.connect()
        if id:
            return await prisma.user.find_unique(
                where={
                    'id' : int(id)
                }
            )
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()



schema = make_federated_schema(schema, query, mutation, user)
app = GraphQL(schema, debug=True)