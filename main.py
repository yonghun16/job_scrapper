from flask import Flask, render_template, request, redirect, send_file
from extractors.remoteok import extract_remoteok_jobs
from extractors.wwr import extract_workremotely_jobs
from export import export_to_file

app = Flask("Job Scrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get('keyword')
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        remoteok_jobs = extract_remoteok_jobs(keyword)
        workremotely_jobs = extract_workremotely_jobs(keyword)
        jobs = remoteok_jobs + workremotely_jobs
        print(jobs)
        if jobs == []:
            return redirect(f"/no-result?keyword={keyword}")
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get('keyword')
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    export_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


@app.route("/no-result")
def no_result():
    keyword = request.args.get('keyword')
    return render_template("no_result.html", keyword=keyword)


app.run("0.0.0.0")
