def export_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w", encoding="utf-8-sig")
    file.write("Position,Comapny,Location,Link\n")
    for job in jobs:
        file.write(
            f"{job['position']},{job['company']},{job['location']},{job['link']}\n"
        )

    file.close()