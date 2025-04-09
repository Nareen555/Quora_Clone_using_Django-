import jwt
import traceback


def create_token(username):
    try:
       
        data = {
            "user_id": f"{username}",
            "username": f"{username}",
            "exp": 1886408464,
            "email": "nareenabc555@gmail.com",
            "orig_iat": 1571048464,
            "customer_id": "9ir5Dg7bvsCA"
        }

        auth_token = jwt.encode(data, "NN_SECRET", algorithm="HS256")
        

        return auth_token

    except IndexError as e:
        traceback.print_exc()
        



def get_username_from_token(token):
    try:
        decoded_token = jwt.decode(token, 'NN_SECRET', algorithms=['HS256'], verify=False)
        return decoded_token.get('username')
    except Exception as error:
        raise error


    

