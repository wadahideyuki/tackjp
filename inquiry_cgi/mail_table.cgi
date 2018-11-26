#!/usr/bin/perl

require 'jcode.pl';
require 'setup.inc';

#---------------------------------------------------------------------------------------------------
# ���M�f�[�^�擾
#---------------------------------------------------------------------------------------------------
	if($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}
	else {
		$buffer = $ENV{'QUERY_STRING'};
	}
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs){
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\t//g;
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		&jcode'convert(*name,'sjis');
		&jcode'convert(*value,'sjis');
		$form{$name} = $value;
		# ���[���A�h���X�擾
		#if($value =~ /@[a-z]/ && $value =~ /\./){$MAIL = $value;}
		if($name eq "E-mail") {
			$MAIL = $value;
		}
		#�����͗����폜����ꍇ�͉��L3�s��#���폜�B
		#if($value eq "") {�@
		#next;
		#}
		$DATA = "$name\t$value\n";
		push(@NEW,$DATA);
	}

#---------------------------------------------------------------------------------------------------
# �K�{�`�F�b�N
#---------------------------------------------------------------------------------------------------
	if(!open(IN,"$g_ErrFile")){ $mes = "�t�@�C��OPEN�G���[�ł��BFileName=[ $g_ErrFile ]";}
	if($mes ne ""){&error;}
		@err = <IN>;
	close(IN);
	$MES = "";
	$MES .= "<table class=\"mail-form\" border=\"0\" cellspacing=\"1\">\n";
	foreach $CK (@NEW){
		chomp $CK;
		($NAME, $VALUE) = split(/\t/,$CK);
		&jcode'convert(*NAME,'euc');

		foreach $ERR (@err){
			$ERR =~ s/\r//g;
			$ERR =~ s/\n//g;
			&jcode'convert(*ERR,'euc');
			if($ERR ne ""){
				if($ERR eq $NAME && $VALUE eq ""){
					&jcode'convert(*ERR,'sjis');
					$MES .= "<tr><td>[<strong class=\"caution\"> $ERR </strong>]�@�̍��ڂ������͂ł��B</td></tr>\n";
					$mes = $MES;
				}
			}
		}
	}
	# ���[���A�h���X�`�F�b�N
	unless($MAIL=~/^[\w\-+\.]+\@[\w\-+\.]+$/i) {
		$MES .= "<tr><td>[<strong class=\"caution\"> E-mail </strong>]�@�̍��ڂ��Ԉ���Ă��܂��B<br>���������[���A�h���X����͂��Ă��������B</td></tr>\n";
		$mes = $MES;
	}
	if($mes ne ""){
		$mes .="</table>\n";
		$mes .="<p class=\"mail-input\"><input type=\"button\" value=\"�@�߁@��@\" onclick=\"JavaScript:history.back();\"></p>";
		&error;
	}

	if($form{'check'} eq "" && $g_Kakunin == 1) {
#---------------------------------------------------------------------------------------------------
# �m�F���
#---------------------------------------------------------------------------------------------------
		print "Content-type:text/html\n\n";
		foreach $CK (@NEW){
			chomp $CK;
			($NAME,$VALUE) = split(/\t/,$CK);
			if($NAME eq "submit") {
				next;
			}
			$strhtml .= "<tr><th>" .$NAME. "</th><td>"  .$VALUE. "</td></tr>\n";
			$strvalue .= "<input type=\"hidden\" name=\"" .$NAME. "\" value=\"" .$VALUE. "\">\n";
		}
		if(!open(IN,"$g_ConfirmHtmlFile")){ $mes = "�t�@�C��OPEN�G���[�ł��BFileName=[ $g_ConfirmHtmlFile ]";}
			if($mes ne ""){&error;}
			@cnfile = <IN>;
		close(IN);
		foreach $FILELINE (@cnfile){
			if($FILELINE =~ /^(.*)<!--%(\w+)%-->(.*)$/) {
				$FILELINE = "";
				$FILELINE .= "<table class=\"mail-form\" border=\"0\" cellspacing=\"1\">\n";
				$FILELINE .= $strhtml;
				$FILELINE .= "</table>\n";
				$FILELINE .= "<p class=\"mail-input\"><input type=\"button\" value=\"�@�߁@��@\" onclick=\"JavaScript:history.back();\">�@<input type=\"button\" value=\"�@���@�M�@\" onclick=\"document.frm.submit();\"></p>\n";
				$FILELINE .= "<form action=\"mail_table.cgi\" method=\"post\" name=\"frm\">\n" .$strvalue. "<input type=\"hidden\" name=\"check\" value=\"1\">\n</form>";
			}
			print $FILELINE;
		}
	}
	else {
#---------------------------------------------------------------------------------------------------
# ���[�����M
#---------------------------------------------------------------------------------------------------
		foreach $lines (@NEW){
			($A,$B) = split(/\t/,$lines);
			if($A eq "check" || $A eq "submit") {
				next;
			}
			$ML_LINE = "$A �F $B\n";
			$ML_DATA .= $ML_LINE;
		}
		if(!open(IN,"$g_ToMailFile")){$mes = '���[���p�t�@�C��OPEN�G���[�ł��Bfile=[ $g_ToMailFile ]';}
		if($mes ne ""){&error;}
			@m_file = <IN>;
		close(IN);
		foreach $M_FILE (@m_file){
			$M_FILE =~ s/<!--%CGI%-->/$ML_DATA/g;
			$MAILDATA .= $M_FILE;
		}
		if(!open(IN,"$g_FroMmailFile")){$mes = '���[���p�t�@�C��OPEN�G���[�ł��Bfile=[ $g_FroMmailFile ]';}
		if($mes ne ""){&error;}
			@m_file = <IN>;
		close(IN);
		foreach $M_FILE (@m_file){
			$M_FILE =~ s/<!--%CGI%-->/$ML_DATA/g;
			$FMAILDATA .= $M_FILE;
		}

		&jcode'convert(*g_SubjectK,'jis');
		&jcode'convert(*g_Subject,'jis');
		if (open(OUT,"| $g_MailCmd -t")) {
			print OUT "MIME-Version: 1.0\n";
			print OUT "Content-Type: text/plain; charset=iso-2022-jp\n";
			print OUT "To: $g_MailTo\n";
			print OUT "From: $MAIL\n";
			print OUT "Subject: $g_Subject\n";
			print OUT "\n\n";
			print OUT "$FMAILDATA\n";
			close(OUT);
		}
		if($MAIL ne "") {
			if (open(OUT,"| $g_MailCmd -t")) {
				print OUT "MIME-Version: 1.0\n";
				print OUT "Content-Type: text/plain; charset=iso-2022-jp\n";
				print OUT "To: $MAIL\n";
				print OUT "From: $g_MailTo\n";
				print OUT "Subject: $g_SubjectK\n";
				print OUT "\n\n";
				print OUT "$MAILDATA\n";
				close(OUT);
			}
		}
#---------------------------------------------------------------------------------------------------
# �f�[�^�x�[�X
#---------------------------------------------------------------------------------------------------
		foreach $DATAS (@NEW){
			($dmy01,$dmy02) = split(/\t/,$DATAS);
			chomp $dmy02;
			if($dmy01 eq "check") {
				next;
			}
			$dmy02 =~ s/\r\n//g;
			push(@DATABASE,$dmy02);
		}

		$NEWDATA = join(',',@DATABASE);

		if(!open(OUT,">>$g_DataFile")){$mes = '�t�@�C���������݃G���[�ł��BFileName=[ $g_DataFile ]';}
		if($mes ne ""){&error;}
			print OUT "$NEWDATA\n";
		close(OUT);
#---------------------------------------------------------------------------------------------------
# ���M��
#---------------------------------------------------------------------------------------------------
		if($g_End == 1) {
			print "Content-type:text/html\n\n";
			foreach $CK (@NEW){
				chomp $CK;
				($NAME,$VALUE) = split(/\t/,$CK);
				if($NAME eq "check" || $NAME eq "submit") {
					next;
				}
				$strhtml .= "<tr><th>" .$NAME. "</th><td>"  .$VALUE. "</td></tr>\n";
			}
			if(!open(IN,"$g_EndHtmlFile")){ $mes = "�t�@�C��OPEN�G���[�ł��BFileName=[ $g_EndHtmlFile ]";}
				if($mes ne ""){&error;}
				@enfile = <IN>;
			close(IN);
			foreach $FILELINE (@enfile){
				if($FILELINE =~ /^(.*)<!--%(\w+)%-->(.*)$/) {
					$FILELINE = "";
					$FILELINE .= "<table class=\"mail-form\" border=\"0\" cellspacing=\"1\">\n";
					$FILELINE .= $strhtml;
					$FILELINE .= "</table>\n";
					$FILELINE .= "<p class=\"mail-input\"><input type=\"button\" value=\"�@�߁@��@\" onclick=\"JavaScript:location.href='$g_ReturnUrl';\"></p>\n";
				}
				print $FILELINE;
			}
		}
		else {
			print "Location: $g_EndUrl\n\n";
		}
	}
	exit;
#---------------------------------------------------------------------------------------------------
# �G���[�֐�
#---------------------------------------------------------------------------------------------------
sub error{
	print "Content-type:text/html\n\n";
	if(!open(IN,"$g_ErrorHtmlFile")){ print "�t�@�C��OPEN�G���[�ł��BFileName=[ $g_ErrorHtmlFile ]\n";}
		@erfile = <IN>;
	close(IN);

	foreach $ERFILES (@erfile){
		$ERFILES =~ s/<!--%CGI%-->/$mes/g;
		print $ERFILES;
	}
	exit;
}
