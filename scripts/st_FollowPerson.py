#!/usr/bin/env python
# -*- coding: utf-8 -*-


#--------------------------------------------------
##指定された人物を追跡するステートマシン
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
            smach.StateMachine.add('FollowPerson', FollowPerson(),
                                   transitions={'exit1':'exit', 
                                                'err_in_speech_rec':'exit'})


#--------------------------------------------------
#--------------------------------------------------
class FollowPerson(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['exit1', 'err_in_speech_rec'])


    def execute(self,userdata):
        #rospy.loginfo(u'ファイル名:'+os.path.basename(__file__)+u'ステート名:'+self.__class__.__name__+u'を実行')
        commonf_dbg_sm_stepin()

        commonf_speech_single('あなたを追跡します。')
        commonf_speech_single('追跡を終了する場合は、ここで止まって。と言ってください。')
        
        Popen(['rosrun', 'common_pkg', 'img_followparson'])
        rospy.sleep(10)

        if commonf_actionf_speech_rec(self.__class__.__name__) == True: #音声認識ノードに現在のステートに対する処理が記述されていた時
            commonf_node_killer('img_followparson')
            commonf_pubf_cam_pan(0)
            commonf_pubf_cam_tilt(0)
            commonf_pubf_cmd_vel(0, 0, 0, 0, 0, 0)

            commonf_dbg_sm_stepout()
            return 'exit1'
        else: #音声認識ノードに現在のステートに対する処理が記述されていない時
            commonf_dbg_sm_stepout()            
            return 'err_in_speech_rec'
