import csv


def send_test_csv_report(test_results):
    a_file = open("test_csv_report.csv", "w")
    writer = csv.writer(a_file)
    for result in test_results:
        for key, value in result.items():
            writer.writerow([key, value])

    a_file.close()