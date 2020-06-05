import web
from excel import Excel

def main():
    #Main
    web.scrape()
    
    xlsx = Excel()

    xlsx.create()

    #open('Config/Insert.txt', 'w').close() -> Commented out for testing
    
    print("Script completed. Good luck job hunting!")
    

if __name__ == "__main__":
    main()
