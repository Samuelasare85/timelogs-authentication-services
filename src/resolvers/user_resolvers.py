from prisma import Prisma
from graphql import GraphQLError
from . import hash_password

# schema = load_schema_from_path('../../schema.graphql')
prisma = Prisma()

#Query Resolvers
def resolve_me(_, info):
    try:
        request = info.context['request']
        user_agent = request.headers.get("user-agent", "guest")
        return user_agent
    except Exception as error:
        raise error

async def resolve_user(obj, info, id:int):
    try:
        await prisma.connect()
        
        user = await prisma.user.find_unique(
            where={
                'id': int(id)
            }
        )
        if not user:
            raise GraphQLError(f'User with id {id} not found')
        return user
    except Exception as error:
            raise error
    finally:
        await prisma.disconnect()

async def resolve_all_users(obj, info):
    try:
        await prisma.connect()
        
        return await prisma.user.find_many(
            order={
                'id': 'asc'
            }
        )
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        
async def resolve_active_users(obj, info):
    try:
        await prisma.connect()
        
        return await prisma.user.find_many(
            where={
                'deleted': False
            },
            order={
                'id': 'asc'
            }
        )
    except Exception as error:
            raise error
    finally:
            await prisma.disconnect()
            
async def resolve_inactive_users(obj, info):
    try:
        await prisma.connect()
        
        return await prisma.user.find_many(
            where={
                'deleted': True
            },
            order={
                'id': 'asc'
            }
        )
    except Exception as error:
            raise error
    finally:
            await prisma.disconnect()
 

        
        
async def resolve_get_users_by_department(obj, info, department):
    try:
        await prisma.connect()
        users = await prisma.user.find_many(
            where={
                'department': department.strip()
            },
            order={
                'id': 'asc'
            }
        )
        if not users:
            raise GraphQLError('Users not found for department')
        return users
    except Exception as error:
            raise error
    finally:
            await prisma.disconnect()
        
# Mutation Resolvers
async def resolve_create_user(obj, info, input):
    try:
        await prisma.connect()
        
        user = await prisma.user.find_unique(
            where={
                'email': input['email'].lower().strip()
            })
        if user:
            raise GraphQLError(f" User with email {input['email']} already exists")
        else:
            first_name = input['first_name'].strip()
            last_name = input['last_name'].strip()
            email = input['email'].lower().strip()
            password = input['password'].strip()
            department = input['department'].strip()
            
            if len(first_name) < 1:       
                raise GraphQLError(f"First name must be at least a character long")
            elif len(last_name) < 1:       
                raise GraphQLError(f"Last name must be at least a character long")
            elif len(password) < 8:
                raise GraphQLError(f"Password must be at least characters long")
            else:
                hashed_password = hash_password.encryptPassword(password)
                newUser = await prisma.user.create(
                data={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': hashed_password,
                    'department': department,
                    })
            return {'message': 'User created successfully', 'user': newUser}
    except Exception as error:
            raise(error)
    finally:
        await prisma.disconnect()
            
        
        
async def resolve_login_user(obj, info, input):
    try:
        await prisma.connect()
        
        user = await prisma.user.find_unique(
            where={
                'email': input['email'].lower().strip()
            })
        if not user:
            raise GraphQLError(f"Account with email {input['email']} does not exist")
        
        email = input['email'].lower().strip()
        password = input['password']
        theUser = await prisma.user.find_unique(
            where={
                'email': email
            })
        isMatch = hash_password.validatePassword(password, theUser.password)
        if not isMatch:
            raise GraphQLError("Incorrect Credentials")
        return {'message': f"User with {email} logged in successfully", 'user': theUser}
        
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        
async def resolve_logout_user(obj, info, email):
    try:
        await prisma.connect()
        
        user = await prisma.user.find_unique(
            where={
                'email': email.lower().strip()
            })
        if not user:
            raise GraphQLError(f"Account with email {email} does not exist")
        
        email = email.lower().strip()
        theUser = await prisma.user.find_unique(
            where={
                'email': email
            })
        return {'message': f"User with {email} is logged out successfully", 'user': theUser}
        
    except Exception as error:
        raise error
    finally:
        await prisma.disconnect()
        
async def resolve_update_user(obj, info, input):
    try:
        await prisma.connect()
        user = await prisma.user.find_unique(
            where={
                'OR':[
                    {
                'email': input['id'].lower().strip()
                    },
                    {
                    'id' : input['id']
                    }
            ]}
        )
        if not user:
            raise GraphQLError(f"Account with email {input['email']} does not exist")
        
        first_name = input['first_name'].strip() or user.first_name
        last_name = input['last_name'].strip() or user.last_name
        email = input['email'].lower().strip() or user.email
        department = input['department'].strip() or user.department
        
        updatedUser = await prisma.user.update(
            where={
                'id': user.id
            },
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'department': department
            }
        )
        return {'message': f"User with {email} is updated successfully", 'user': updatedUser} 
    except Exception as error:
            raise error
    finally:
        await prisma.disconnect()
        
async def resolve_delete_user(obj, info, email):
    try:
        await prisma.connect()
        user = await prisma.user.find_unique(
            where={
                'email': email.lower().strip()
            }
        )
        if not user:
            raise GraphQLError(f"Account with email {input['email']} does not exist")
        
        email = email.lower().strip()
        deletedUser = await prisma.user.delete(
            where={
                'email': email
            }
        )
        return {'message': f"User with {email} is deleted successfully"}
    except Exception as error:
            raise error
    finally:
        await prisma.disconnect()
        
        

