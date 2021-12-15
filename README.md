# Extractentity
Questionanswering module

Command to launch the api .

  python extract.py

Make sure to install all required packages with specified versions

Below are the input and output of the module

Input:
{
    "Input": "Hi,Please quote renewal and upgrade user tier for the items below:Product-J Software Premium Upgrade Tier: 1800 users to 3000 User license Tempo Timesheets - time tracking & reports cloud Upgrade Tier: 1800 users to 3000 User license Thank you."
}


Output : 

[{'Product': 'product-j', 'Score': 0.552757740020752, 'Users': '1800'}]
