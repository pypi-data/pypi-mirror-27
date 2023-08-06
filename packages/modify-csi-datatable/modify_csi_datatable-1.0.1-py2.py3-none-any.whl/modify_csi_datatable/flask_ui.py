from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_file, send_from_directory
import os
from sys import version_info
import logging
from tempfile import mkdtemp
from zipfile import ZipFile

if version_info.major == 3 and version_info.minor == 5:
    from modify_csi_datatable import modify_fw_datatable
    from modify_cfg_file import modify_cfg_file
elif version_info.major == 3 and version_info.minor == 6:
    from modify_csi_datatable import modify_fw_datatable
    from modify_cfg_file import modify_cfg_file

app = Flask('modify_csi_datatable')
# app.config.from_object(__name__)

logger = app.logger
logger.setLevel(logging.DEBUG)

# configure logger
handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
handler_stream = logging.StreamHandler()
handler_stream.setFormatter(handler_stream_formatter)
handler_stream.setLevel(logging.DEBUG)
logger.addHandler(handler_stream)

logger.debug('Python version is: {}'.format(version_info))

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='UpB3e0sg8och4mVp5kb60vUTAsY2JsuXeiO4Og1k82hYAdYjTY',
    USERNAME='admin',
    PASSWORD='default',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    logger.debug('New Interval is: {}'.format(request.form['interval']))
    logger.debug('New Name is: {}'.format(request.form['dt_name']))

    dt_name = request.form['dt_name']
    dt_interval = request.form['interval']
    user_initials = request.form['user_initials']

    # TODO: check for user intials
    # if request.form['user_initials'] is not '':
    logger.info('The user {} is performing the conversion'.format(request.form['user_initials']))
    # else:
    #     flash('Please enter your intials')
    #     return render_template('upload_file.html')

    with ZipFile(os.path.join(session['tmp_dir'], session['project_name'] + '.zip'), 'a') as zip_fid:
        for dirpath, dirnames, filenames in os.walk(session['tmp_dir']):
            for file in filenames:
                file_name, file_extension = os.path.splitext(file)

                if file_extension in ['.cfg']:
                    logger.info('Updating the {} file'.format(file))
                    cfg_filepath = os.path.join(session['tmp_dir'], file)
                    logger.info('Looking in {}'.format(cfg_filepath))
                    modify_cfg_file(
                        cfg_filepath=cfg_filepath,
                        user_initials=user_initials,
                        repl_tablename=dt_name,
                        interval=dt_interval,
                        units="MIN"
                    )
                    zip_fid.write(os.path.join(session['tmp_dir'], file), arcname=file)

                elif file_extension.lower() in ['.cr1', '.cr8', '.cr300', '.cr6']:
                    logger.info('Updating the {} file'.format(file))
                    modify_fw_datatable(
                        proj_filepath=os.path.join(session['tmp_dir'], file),
                        user_initials=user_initials,
                        repl_tablename=dt_name,
                        interval=dt_interval
                    )
                    zip_fid.write(os.path.join(session['tmp_dir'], file), arcname=file)

    logger.info('Sending the zip file: {}'.format(session['project_name'] + '.zip'))

    return send_from_directory(
        session['tmp_dir'], session['project_name'] + '.zip', mimetype='application/zip', as_attachment=True
    )


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        logger.debug('{}'.format(request.files))
        logger.debug('{}'.format(type(request.files)))

        for key, f in request.files.items():
            if key.startswith('file'):
                # logger.debug('Saving {} to {}'.format(f.filename, app.config['UPLOAD_FOLDER']))
                # f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                logger.info('Saving {} to {}'.format(f.filename, session['tmp_dir']))
                f.save(os.path.join(session['tmp_dir'], f.filename))
                session['project_name'], extension = os.path.splitext(f.filename)

    return render_template('upload_file.html')


@app.route('/')
def modify_csi_datatable():
    session['tmp_dir'] = mkdtemp()

    logger.debug('Created the temp directory: {}'.format(session['tmp_dir']))
    return render_template('upload_file.html')


if __name__ == '__main__':
    app.run(debug=True)
