#!/usr/bin/env python
# -*- coding: utf-8 -*-


#--------------------------------------------------
#質問の答えを教えるステートマシン
#
#author: Yuta KIYAMA
#date: 16/03/12
#--------------------------------------------------


import sys
import roslib
sys.path.append(roslib.packages.get_pkg_dir('common_pkg') + '/scripts/common')

from common_import import *
from common_function import *


#--------------------------------------------------
#ステートマシン設計規則
#--------------------------------------------------
#ステートを跨ぐデータはパラメータ(/param/以下)に保存する


#--------------------------------------------------
#このファイル内のステートマシンの宣言部分
#--------------------------------------------------
class MainState(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['exit'])
        with self:
        #以降にステートを追加
            smach.StateMachine.add('TelltoPerson', TelltoPerson(),
                                   transitions = {'exit1':'exit'})


class TelltoPerson(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['exit1'])


    def execute(self,userdata):
        #rospy.loginfo(u'ファイル名:'+os.path.basename(__file__)+u'ステート名:'+self.__class__.__name__+u'を実行')
        commonf_dbg_sm_stepin()        

        answer=rospy.get_param('/param/ans')
        commonf_speech_single(answer)

        commonf_dbg_sm_stepout()
        return 'exit1'
