import web
from excel import Excel

def main():
    #Main
    web.scrape()
    
    xlsx = Excel()

    xlsx.create()
    print("Script completed. Good luck job hunting!")
    

if __name__ == "__main__":
    main()
