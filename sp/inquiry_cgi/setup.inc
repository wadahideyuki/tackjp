#!/usr/bin/perl -w

############################################################
# ��
############################################################
# ���[���R�}���h(���ɍ��킹�ĕς��Ă�������)
$g_MailCmd = '/usr/sbin/sendmail';

############################################################
# �ύX�s��
############################################################
# �쐬�t�@�C���̃p�X
$g_DataFile = './data/data.csv';
# �G���[�\�����f�i�[�t�@�C��
$g_ErrFile = './data/error.dat';
# �G���[�g�s�l�k
$g_ErrorHtmlFile = './error.html';
# �m�F�g�s�l�k
$g_ConfirmHtmlFile = './confirm.html';
# �I���g�s�l�k
$g_EndHtmlFile = './end.html';
# �X�ܗl�ɑ��郁�[���x�[�X
$g_ToMailFile = './data/tomail.txt';
# �ڋq�l�ɑ��郁�[���x�[�X
$g_FroMmailFile = './data/frommail.txt';

############################################################
# �ݒ�
############################################################
# ���[�����M��i���[�����΂���̃A�h���X�ł��j�����i��Ftest1@cns-inc.co.jp;test2@cns-inc.co.jp�j
$g_MailTo = 'info@tack-ic.jp';
# �X�܌����i�X�܂ɓ͂����[���̌����ł��j
$g_Subject = '���₢���킹';
# �ڋq�����i�ڋq�ɓ͂����[���̌����ł��j
$g_SubjectK = '���₢���킹�����������肪�Ƃ��������܂���';
# ���[�����M��̂t�q�k�i���[�����M��̂t�q�k�ł��j
$g_EndUrl = 'http://www.tack-ic.jp';
# �߂��̂t�q�k
$g_ReturnUrl = 'http://www.tack-ic.jp';

# �m�F��ʂɗL���i�m�F��ʂ��K�v�Ȃ�΁u1�v���A����Ȃ��Ȃ�΁u0�v������Ă��������B�j
$g_Kakunin = 1;
# ���M��̏����i�I����ʂ��K�v�Ȃ�΁u1�v���A���M��t�q�k�ɔ�΂��Ȃ�΁u0�v������Ă��������B�j
$g_End = 1;

############################################################
# �F�ݒ�
############################################################
# �e�[�u���{�[�_�[�J���[
$g_TableBorderColor = '#000000';
# ���ڂ̃o�b�N�J���[
$g_LavelBackColor ='#ffffff';
# �l�̃o�b�N�J���[
$g_DataBackColor ='#ffffff';
# ���ڂ̕����F
$g_LavelTextColor ='#000000';
# �l�̕����F
$g_DataTextColor ='#000000';

true;