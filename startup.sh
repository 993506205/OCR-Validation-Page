echo "Creating virtualenv and installing needed modules.."
virtualenv .env && source .env/Scripts/activate && pip install -r requirements.txt
read -rsn1 -p"Press any key to continue..";echo