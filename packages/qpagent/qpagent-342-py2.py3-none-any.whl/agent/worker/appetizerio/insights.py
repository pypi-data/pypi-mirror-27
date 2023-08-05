#!/usr/bin/env python3
#
# Copyright 2017 AppetizerIO (https://appetizer.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import os
import subprocess
import sys
import time
import zipfile

try:
    import requests
    from qiniu import put_file, etag
    import qiniu.config
except ImportError:
    print('please install dependencies from requirements.txt')
    sys.exit(1)

try:
    import zlib

    COMPRESS = zipfile.ZIP_DEFLATED
except ImportError:
    print('python zlib is not available, which is highly suggested')
    COMPRESS = zipfile.STORED

CONFIG = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG, 'r') as f:
    config = json.loads(f.read())
ANXIETY = config['anxiety']
API_BASE = config['api_base']
TOKEN_PATH = os.path.join(os.path.dirname(__file__), '.access_token')
APKDUMP = os.path.join(os.path.dirname(__file__), 'apkdump.js')
DEVICE_LOG_BASE = config['device_log_location']
try:
    subprocess.check_output(['node', '-v']);
except:
    print('Node.js is not installed and some functionality might not work properly')


def version(args):
    print('1.2.2')


def get_apk_manifest(apk):
    return subprocess.check_output(['node', APKDUMP, apk]).decode('utf-8')


def get_apk_package(apk):
    manifest = get_apk_manifest(apk)
    return json.loads(manifest)['package']


def adb(cmd, d=None, showCmd=False):
    dselector = [] if d is None else ['-s', d]
    fullCmd = ['adb'] + dselector + cmd
    if showCmd: print(fullCmd)
    return subprocess.check_call(fullCmd)


def _load_token():
    access_token = ''
    try:
        with open(TOKEN_PATH, 'r') as tokenfile:
            access_token = tokenfile.readline()
            if access_token == '':
                print('no stored access token, please login')
                return None
    except:
        print('no stored access token, please login')
        return None
    authorization = 'Bearer ' + access_token
    r = requests.get(API_BASE + '/oauth/check_token', headers={'Authorization': authorization}, verify=False)
    if r.status_code != 200:
        print(r.json())
        print('stored access token is no longer valid, please login again')
        return None
    print('valid access token: ' + access_token)
    return access_token


def login(username, password):
    r = requests.post(API_BASE + '/oauth/access_token',
                      data={
                          'grant_type': 'password',
                          'username': username,
                          'password': password
                      }, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic YXBwZXRpemVyX2NsaWVudDppbnRlcm5hbA=='
        }, verify=False)
    if r.status_code != 200:
        print('Failed to login. User does not exist or bad password')
        return 1
    access_token = r.json()['access_token']
    with open(TOKEN_PATH, 'w') as tokenfile:
        tokenfile.write(access_token)
    print('Login succeeded')
    print('access token: ' + access_token)
    print('access token persisted, subsequent commands will be properly authenticated with this token')
    print('token will be valid for the following 60 days and will get renewed if any command is executed')


def logout(args):
    try:
        with open(TOKEN_PATH, 'w') as tokenfile:
            tokenfile.write('')
    except:
        pass
    print('Bye')


def is_fortified(apk, *args, **kwargs):
    with zipfile.ZipFile(apk) as zip_obj:
        solist = [s.rsplit('/')[-1] for s in zip_obj.namelist() if s.endswith('.so')]
    packer = None
    if 'libexecmain.so' in solist and 'libexec.so' in solist:
        packer = 'aijiami'
    elif 'libDexHelper.so' in solist and 'libDexHelper-x86.so' in solist:
        packer = 'bangbang enterprise'
    elif 'libsecmain.so' in solist and 'libsecexe.so' in solist:
        packer = 'bangbang'
    elif 'libtup.so' in solist or 'libexec.so' in solist:
        packer = 'tencent'
    elif ('libprotectClass.so' in solist and 'libprotectClass_x86.so' in solist) or (
                    'libjiagu.so' in solist and 'libjiagu_art.so' in solist) or (
                    'libjiagu.so' in solist and 'libjiagu_x86.so' in solist):
        packer = '360'
    elif 'libbaiduprotect.so' in solist and 'ibbaiduprotect_x86.so' in solist:
        packer = 'baidu'
    elif ('libddog.so' in solist and 'libfdog.so' in solist) or 'libchaosvmp.so' in solist:
        packer = 'najia'
    elif 'libnqshieldx86.so' in solist and 'libnqshield.so' in solist:
        packer = 'netqin'
    elif 'libmobisec.so' in solist or 'libmobisecx.so' in solist:
        packer = 'alibaba'
    elif 'libegis.so' in solist:
        packer = 'tongfudun'
    elif 'libAPKProtect.so' in solist:
        packer = 'apkprotect'
    elif any('libshell' in s for s in solist):
        packer = 'tencent_legu'
    return packer


def process(apk, processed_apk):
    access_token = _load_token()
    if access_token is None:
        print('Please login to AppetizerIO first')
        return 1
    # validate APK file
    try:
        manifest = json.loads(get_apk_manifest(apk))
    except:
        print('not a valid APK')
        return 1
    with zipfile.ZipFile(apk) as checkf:
        try:
            checkf.getinfo('assets/appetizer.cfg')
            print('input APK is already instrumented')
            return 1
        except:
            pass
    if is_fortified(apk) is not None:
        print("the apk is fortified")
        return 1
    permissions = [p['name'] for p in manifest['usesPermissions']]
    if 'android.permission.WRITE_EXTERNAL_STORAGE' not in permissions:
        print("the apk does not have READ/WRITE external storage permission")
        return 1
    components = manifest['application']['activities'] + manifest['application']['services'] + manifest['application'][
        'receivers']
    processes = list(set([p['process'] for p in components if 'process' in p]))
    if len(processes) > 1:
        print(
            "WARNING: the apk launches multiple processes. multi-process support is not complete and could be problematic with Appetizer")

    authorization = 'Bearer ' + access_token
    original_name = os.path.basename(apk)
    pkg = get_apk_package(apk)
    token = None
    print('0. request Appetizer Insights upload permission')
    r = requests.post(API_BASE + '/insight/process/qiniu', headers={'Authorization': authorization}, verify=False)
    r_json = r.json()
    print(r_json)
    if r.status_code != 200:
        print(r_json['msg'])
        return 1
    token = r_json['token']
    key = r_json['key']

    print('1. upload APK file')
    print('apk: ' + apk)
    print('pkg: ' + pkg)
    print('upload......')
    ret, info = put_file(token, key, apk)
    print(ret)
    if ret is None or 'success' not in ret or ret['success'] != True:
        print('upload error')
        return 1

    print('2. wait for the APK to be processed')
    r_json = None
    while True:
        r = requests.get(API_BASE + '/insight/process', headers={'Authorization': authorization}, params={'key': key})
        r_json = r.json()
        if r_json['success'] != True:
            print(r_json)
            return 1
        if r_json['state'] == 'return_upload_auth' or r_json['state'] == 'upload_finish' or r_json[
            'state'] == 'server_download':
            print('waiting...... server is downloading the APK')
        elif r_json['state'] == 'rewriting':
            print('waiting...... server is processing the APK')
        elif r_json['state'] == 'rewrite_success' or r_json['state'] == 'server_upload':
            print('waiting...... server is uploading the processed APK')
        elif r_json['state'] == 'server_upload_success':
            print('server has completed processing the APK')
            break
        else:
            print(r_json)
            print('server fails to process the APK')
            return 1
        time.sleep(ANXIETY)
    print(r_json)
    downloadURL = r_json['downloadURL']
    print(downloadURL)

    print('3. download processed APK')
    r = requests.get(downloadURL)
    if r.status_code != 200:
        print('download failed')
        return 1
    print('download completed')
    with open(processed_apk, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024000):
            f.write(chunk)
    return key


def install(apk, serialnos):
    try:
        adb(['version'])
    except:
        print('adb not available')
        return 1
    pkg = get_apk_package(apk)
    serialnos = serialnos if len(serialnos) > 0 else [None]
    print(
        'This command is not useful for MIUI devices; please click on the installation popup dialog and manually grant WRITE_EXTERNAL_STROAGE permission')
    print('1. install processed APK')
    for d in serialnos:
        adb(['uninstall', pkg], d)
        adb(['install', apk], d)  # Note: Xiaomi will pop up a dialog
    print('APK installed')

    print('2. grant permissions for logging')
    for d in serialnos:
        adb(['shell', 'pm', 'grant', pkg, 'android.permission.WRITE_EXTERNAL_STORAGE'], d, True)
        adb(['shell', 'pm', 'grant', pkg, 'android.permission.READ_EXTERNAL_STORAGE'], d, True)
    print('permission granted with adb, please double check')


def analyze(apk, serialnos, clear=False):
    try:
        adb(['version'])
    except:
        print('adb not available')
        return 1
    access_token = _load_token()
    if access_token is None:
        print('Please login to AppetizerIO first')
        return 1
    authorization = 'Bearer ' + access_token
    pkg = get_apk_package(apk)
    with open('AndroidManifest.json', 'wb') as f:
        f.write(get_apk_manifest(apk).encode('utf-8'))
    log_zip = pkg + '.log.zip'
    serialnos = serialnos if len(serialnos) > 0 else [None]
    DEVICE_LOG = DEVICE_LOG_BASE + pkg + '.log'
    token = None
    print('0. harvest and compress device logs')
    with zipfile.ZipFile(log_zip, 'w') as myzip:
        myzip.write('AndroidManifest.json', compress_type=COMPRESS)
        for d in serialnos:
            fname = d if d is not None else "devicelog"
            try:
                adb(['pull', DEVICE_LOG, fname + '.log'], d)
            except:
                print(
                    'failed to retrieve logs from a device, please double check if the app ha the permission to log to SDCARD')
            if clear:
                adb(['shell', 'echo>' + DEVICE_LOG], d)
            myzip.write(fname + '.log')
    os.remove('AndroidManifest.json')

    print('1. request analysis from the server')
    r = requests.post(API_BASE + '/insight/analyze/qiniu', headers={'Authorization': authorization},
                      data={'pkgName': pkg}, verify=False)
    r_json = r.json()
    print(r_json)
    if r.status_code != 200:
        print(r_json)
        return 1
    token = r_json['token']
    key = r_json['key']

    print('2. upload log files')
    print('pkg: ' + pkg)
    print('log file: ' + log_zip)
    print('uploading......')
    ret, info = put_file(token, key, log_zip)
    if (ret is None or 'success' not in ret or ret['success'] != True):
        print('upload error')
        return 1

    print('3. server analyzing')
    r_json = None
    while True:
        r = requests.get(API_BASE + '/insight/analyze', headers={'Authorization': authorization}, params={'key': key})
        r_json = r.json()
        if r_json['success'] != True:
            print(r_json)
            return 1
        if r_json['state'] == 'return_upload_auth' or r_json['state'] == 'upload_finish' or r_json[
            'state'] == 'server_download':
            print('waiting...... server is downloading log')
        elif r_json['state'] == 'analyzing':
            print('waiting...... server is analyzing')
        elif r_json['state'] == 'analyze_success' or r_json['state'] == 'report_exporting':
            print('waiting...... server is exporting the report')
        elif r_json['state'] == 'report_export_success' or r_json['state'] == 'server_upload':
            print('waiting...... server is uploading the report')
        elif r_json['state'] == 'server_upload_success':
            print('server has generated and uploaded the report')
            if 'reportExport' in r_json:
                print('exported reports available at:')
                print(r_json['reportExport'])
            break
        else:
            print(r_json)
            print('server fails to analyze the logs')
            return 1
        time.sleep(ANXIETY)

    print('4. cleanup')
    os.remove(log_zip)
    for d in serialnos:
        if d is None:
            os.remove('devicelog.log')
        else:
            os.remove(d + '.log')

    print('All done! You can now view the report via Appetizer Desktop')
    if not clear:
        print('Please remember to delete old logs with clearlog command to avoid repeated analysis')
    return key


def clearlog(apk, serialnos):
    try:
        pkg = get_apk_package(apk)
        serialnos = serialnos if len(serialnos) > 0 else [None]
        DEVICE_LOG = DEVICE_LOG_BASE + pkg + '.log'
        for d in serialnos:
            adb(['shell', 'echo>' + DEVICE_LOG], d)
        print('done')
    except Exception:
        pass


    # if __name__ == '__main__':
    # login('elemeqa', 'eleme517517')
    # process('/Users/mafei/Downloads/android_62bb0856b3e320ae4f4cca49eb741734.apk', 'instrumented.apk')
    # install('/Users/mafei/eleme.qa/qualityplatform.agent/agent/worker/appetizerio/instrumented.apk', {'GWY0217414001213'})
    # clearlog('instrumented.apk', {'GWY0217414001213'})
    # analyze('instrumented.apk', {'GWY0217414001213'})
