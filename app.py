# from scrap import main, extract_filename_from_url
# import os
# from flask import Flask, render_template, request, send_file, Response, after_this_request, flash, redirect, url_for
# from werkzeug.utils import secure_filename

from scrap import main, extract_filename_from_url
import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = os.urandom(16)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        website_url = request.form.get("website-url")
        main(website_url)
        return render_template(
            "index.html", file_name=extract_filename_from_url(website_url)
        )
    return render_template("index.html")



# # Configure upload directory (adjust as needed)
# UPLOAD_FOLDER = 'report-files'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Function to validate and secure filenames
# def allowed_file(filename):
#     allowed_extensions = {'csv'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# @app.route('/download-csv/<file_name>')
# def download_csv(file_name):
#     csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name) + '.csv')
#     print(f"Downloading file from: {csv_path}")

#     try:
#         # Check if file exists before attempting download
#         if not os.path.exists(csv_path):
#             flash("File not found. Please generate the CSV file first.")
#             return "", 404  # Return empty response with 404

#         @after_this_request
#         def cleanup(response):
#             if response.status_code == 200:
#                 import time
#                 time.sleep(10)
#                 try:
#                     os.remove(csv_path)
#                     flash("File downloaded and deleted successfully.")
#                 except Exception as error:
#                     app.logger.error("Error removing downloaded file handle", error)
#                     flash("Error deleting downloaded file. Please contact the administrator.")

#         return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name=f'{file_name}.csv')
#     except Exception as error:
#         flash(f"An error occurred: {error}")
#         return redirect(url_for('handle_error'))  # Placeholder route

# # Basic placeholder routes (replace with your actual logic)
# @app.route('/generate_csv')
# def generate_csv():
#     flash("This is a placeholder route for CSV generation. Implement your logic here.")
#     return "", 404  # Return empty response with 404 status code

# @app.route('/handle_error')
# def handle_error():
#     flash("This is a placeholder route for error handling. Implement your logic here.")
#     return "Error handling route not implemented yet."




# @app.route('/download-csv/<file_name>')
# def download_csv(file_name):
#   csv_path = f'{file_name}.csv'
#   try:
#     response = send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name=f'{file_name}.csv')
#     # Delete the file after the download completes
#     def delete_file():
#       print('inside delete')
#       try:
#         os.remove(csv_path)
#       except Exception as error:
#         app.logger.error("Error removing downloaded file", error)
#     response.finish_callback = delete_file
#     return response
#   except FileNotFoundError:
#     return "File not found. Please generate the CSV file first."


# @app.route('/download-csv/<file_name>')
# def download_csv(file_name):
#   csv_path = f'{file_name}.csv'
#   try:
#     response = send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name=f'{file_name}.csv')
#     # Delete the file after the download completes
#     import time
#     time.sleep(5)
#     delete_file(csv_path)
#     return response
#   except FileNotFoundError:
#     return "File not found. Please generate the CSV file first."

# def delete_file(csv_path):
#     print('I am inside delete')
#     try:
#         os.remove(csv_path)
#     except Exception as error:
#         app.logger.error("Error removing downloaded file", error)



# It can download but not delete after downloading is completed. and does not throw any error.
@app.route('/download-csv/<file_name>')
def download_csv(file_name):
  csv_path = f'{file_name}.csv'
  try:
    response = send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name=f'{file_name}.csv')
    # Delete the file after the download completes
    def delete_file():
      try:
        os.remove(csv_path)
      except Exception as error:
        app.logger.error("Error removing downloaded file", error)
    response.finish_callback = delete_file
    return response
  except FileNotFoundError:
    return "File not found. Please generate the CSV file first."


# It can download but not delete after downloading is completed and throw error. Why? Is it because we forget to call the cleanup function?
# @app.route('/download-csv/<file_name>')
# def download_csv(file_name):
#     csv_path = f'{file_name}.csv'
#     print(csv_path)

#     @after_this_request
#     def cleanup(response):
#         if response.status_code == 200:
#             try:
#                 os.remove(csv_path)
#             except Exception as error:
#                 app.logger.error("Error removing downloaded file handle", error)
#         return response

#     try:
#         return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name=f'{file_name}.csv')
#     except FileNotFoundError:
#         return "File not found. Please generate the CSV file first."


# It can delete but not download
# @app.route('/download-csv/<file_name>')
# def download_csv(file_name):
#     csv_path = f'{file_name}.csv'

#     @after_this_request
#     def remove_file(response):
#         try:
#             os.remove(csv_path)
#         except Exception as error:
#             app.logger.error("Error removing downloaded file handle", error)
#         return response

#     def generate():
#         with open(csv_path, 'rb') as f:
#             yield from f

#     r = Response(generate(), mimetype='text/csv')
#     r.headers.set('Content-Disposition', 'attachment', filename=f'{file_name}.csv')
#     return r


if __name__ == "__main__":
    app.run(debug=True)
