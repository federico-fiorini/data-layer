##TD LIMPO - DATA LAYER

RESTful APIs - Connected to PostgreSQL database

####HOW TO SET UP
    # Set up virtualenv
    ./deploy.sh
    
    # Activate virtual environment
    source .env/bin/activate

    # Set up environment variables
    export AUTHORIZATION_KEY=secret_token
    export POSTGRE_USERNAME=postgres
    export POSTGRE_PASSWORD=postgres
    export POSTGRE_HOST=localhost
    export POSTGRE_DATABASE=td-limpo
    
    # Exit virtual environment
    deactivate

####HOW TO RUN
    ./run.py