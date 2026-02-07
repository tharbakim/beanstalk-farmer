if __name__ == "__main__":
    import dotenv
    import os
    dotenv.load_dotenv()
    from src.server import app, get_bean_client

    # Attempt to construct the beanstalk client and print a startup debug
    # message so it's easy to see whether the client was able to connect.
    client, err = get_bean_client()
    bean_host = os.getenv('BEANSTALK_HOST', 'localhost')
    bean_port = os.getenv('BEANSTALK_PORT', '11300')
    if client:
        print(f'Beanstalk client connected to {bean_host}:{bean_port}')
    else:
        print(f'Beanstalk client connection failed: {err}')

    app.run(host=os.getenv('BEANSTALK_FARMER_HOST'), port=os.getenv('BEANSTALK_FARMER_PORT'), debug=bool(os.getenv('BEANSTALK_FARMER_DEBUG')))
