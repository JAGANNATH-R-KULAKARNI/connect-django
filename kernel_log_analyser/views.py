from django.shortcuts import render
from django.http import HttpResponse
import datetime
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

type_map={55: 'authentication',
 56: 'check',
 76: 'session',
 5: 'ALERT',
 57: 'connection',
 47: 'User',
 59: 'cupsd',
 39: 'Received',
 7: 'Authentication',
 28: 'Kerberos',
 66: 'logrotate:',
 58: 'cups:',
 0: '',
 17: "Couldn't",
 6: 'ANONYMOUS',
 69: 'notify',
 60: 'getpeername',
 79: 'warning:',
 77: 'syslogd',
 30: 'Linux',
 8: 'BIOS-provided',
 1: '0MB',
 2: '126MB',
 80: 'zapping',
 65: 'klogd',
 34: 'On',
 62: 'irqbalance',
 18: 'DMI',
 3: 'ACPI',
 51: 'You',
 10: 'Built',
 29: 'Kernel',
 67: 'mapped',
 25: 'Initializing',
 11: 'CPU',
 71: 'portmap',
 36: 'PID',
 20: 'Detected',
 50: 'Version',
 48: 'Using',
 73: 'rpc.statd',
 16: 'Console:',
 31: 'Memory:',
 13: 'Calibrating',
 41: 'Security',
 40: 'SELinux:',
 44: 'There',
 23: 'Failure',
 75: 'selinux_register_security:',
 14: 'Capability',
 72: 'rpc.idmapd',
 19: 'Dentry',
 26: 'Inode-cache',
 32: 'Mount-cache',
 12: 'CPU:',
 27: 'Intel',
 22: 'Enabling',
 15: 'Checking',
 37: 'POSIX',
 33: 'NET:',
 35: 'PCI:',
 68: 'mtrr:',
 4: 'ACPI:',
 43: 'Starting',
 78: 'usbcore:',
 46: 'Transparent',
 52: 'apm:',
 54: 'audit:',
 64: 'kernel.core_uses_pid',
 24: 'HCI',
 61: 'hcid',
 53: 'audit(1122475266.4294965305:0):',
 42: 'Setting',
 74: 'sdpd',
 45: 'Total',
 9: 'Bringing',
 49: 'VFS:',
 21: 'Dquot-cache',
 70: 'pci_hotplug:',
 63: 'isapnp:',
 38: 'Real'}

def home_page(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    #C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser

    # cv=CountVectorizer()
    le = LabelEncoder()

    with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
        le.classes_ = label
        print('Label Encoder')
        print(le)
    with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
        print('count vectorizer pickle')
        cv=joblib.load(vect_pickle)
        print(cv)
        
                
    with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\kernel_log_analyser','rb') as f:
        print('ok')
        knn_pickle_model=pickle.load(f)
        data=['closed for user test']
        vect=cv.transform(data).toarray()
        print(knn_pickle_model.predict(vect))
        # predictions_test = le.inverse_transform(knn_pickle_model.predict(vect))
        print(type_map[knn_pickle_model.predict(vect)[0]])
        print(vect)
        
    return HttpResponse(html)