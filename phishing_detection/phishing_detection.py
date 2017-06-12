import sys, getopt
from integrate import integrate
from calculate_probability import calculate_probability

########
# Usage
# python phishing_detection.py -u <url> -i <input_file> -o <output_file>
########

DEFAULT_URL = "https://www.naver.com/"
DEFAULT_INPUT_FILE_PATH = "files/urls.csv"
DEFAULT_OUTPUT_FILE_PATH = "files/results.csv"

def call_integrate(url):
    try:
        return integrate(url)
    except:
        print("Error(001): integrate() failed")

def call_integrate_for_file(input_file_path, output_file_path):
    with open(input_file_path, "r") as input_file:
        with open(output_file_path, "w") as output_file: # this causes error when calling from a different path
            # write header
            output_file.write("url,verdict\n")

            # call integrate for each url
            urls = input_file.readlines()
            for url in urls:
                url = url.rstrip()
                result = call_integrate(url)
                output_file.write(url + "," + result + "\n")
        output_file.close()
    input_file.close()

def main(argv):
    url = DEFAULT_URL
    has_input_file = False
    has_output_file = False
    input_file_path = DEFAULT_INPUT_FILE_PATH
    output_file_path = DEFAULT_OUTPUT_FILE_PATH

    try:
        opts, args = getopt.getopt(argv, "hu:i:o:p", ["help", "url=", "inputfile=", "outputfile=", "probability="])
    except getopt.GetoptError:
        print("Error(000): invalid options")
        print("phishing_detection.py -u <url> -i <input_file> -o <output_file> -p <probability>")
        return

    if (not opts):
        print("Running script on default url.")
        call_integrate(url)
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print("phishing_detection.py -u <url> -i <input_file> -o <output_file>")
                return
            elif opt in ("-u", "--url"):
                url = arg
                call_integrate(url)
            elif opt in ("-i", "--inputfile"):
                has_input_file = True
                input_file_path = arg
            elif opt in ("-o", "--outputfile"):
                has_output_file = True
                output_file_path = arg
            elif opt in ("-p", "--probability"): # include inputfile and outputfile path for this option too
                calculate_probability()

        if (has_output_file and not has_input_file):
            print("Error(002): requires input_file")
        if (has_input_file):
            call_integrate_for_file(input_file_path, output_file_path)

if __name__ == "__main__":
    print("===============Starting phishing_detection.py===============")
    main(sys.argv[1:])
    print("===============Finishing phishing_detection.py==============")
