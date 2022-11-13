email_unregistered_error_page = """
    <head>
        <style>
            body {
                background-color: #f2f2f2;
            }

            h2 {
                font-family: Arial, Helvetica, sans-serif;
                color: red;
                text-align: center;
            }

            .center {
                text-align: center;
                margin: 0;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding-top: 5%;
            }
        
            .button {
                border: none;
                color: white;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }

            .button1 {
                background-color: black;
                color: white;
            }

            .button1:hover {
                background-color: rgb(0, 0, 0);
                color: white;
                box-shadow: 0px 15px 20px rgba(100, 100, 100, 0.4);
                transform: translateY(-7px);
            }
        </style>
    </head>

    <body>
        <div class="center">
            <h2>Email is unregistered. Try Signing Up!</h2>
            <a href="/" class="button button1">Try Again!</a>
        </div>
    </body>
    """

email_registered_error_page = """
    <head>
        <style>
            body {
                background-color: #f2f2f2;
            }

            h2 {
                font-family: Arial, Helvetica, sans-serif;
                color: red;
                text-align: center;
            }

            .center {
                text-align: center;
                margin: 0;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding-top: 5%;
            }
        
            .button {
                border: none;
                color: white;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }

            .button1 {
                background-color: black;
                color: white;
            }

            .button1:hover {
                background-color: rgb(0, 0, 0);
                color: white;
                box-shadow: 0px 15px 20px rgba(100, 100, 100, 0.4);
                transform: translateY(-7px);
            }
        </style>
    </head>

    <body>
        <div class="center">
            <h2>Email is already registered. Try Logging in!</h2>
            <a href="/" class="button button1">Try Again!</a>
        </div>
    </body>
    """

email_invalid_error_page = """
    <head>
        <style>
            body {
                background-color: #f2f2f2;
            }

            h2 {
                font-family: Arial, Helvetica, sans-serif;
                color: red;
                text-align: center;
            }

            .center {
                text-align: center;
                margin: 0;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding-top: 5%;
            }
        
            .button {
                border: none;
                color: white;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }

            .button1 {
                background-color: black;
                color: white;
            }

            .button1:hover {
                background-color: rgb(0, 0, 0);
                color: white;
                box-shadow: 0px 15px 20px rgba(100, 100, 100, 0.4);
                transform: translateY(-7px);
            }
        </style>
    </head>

    <body>
        <div class="center">
            <h2>Email is invalid...</h2>
            <a href="/" class="button button1">Try Again!</a>
        </div>
    </body>
    """