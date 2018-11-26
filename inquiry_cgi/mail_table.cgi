#!/usr/bin/perl

require 'jcode.pl';
require 'setup.inc';

#---------------------------------------------------------------------------------------------------
# 送信データ取得
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
		# メールアドレス取得
		#if($value =~ /@[a-z]/ && $value =~ /\./){$MAIL = $value;}
		if($name eq "E-mail") {
			$MAIL = $value;
		}
		#未入力欄を削除する場合は下記3行の#を削除。
		#if($value eq "") {　
		#next;
		#}
		$DATA = "$name\t$value\n";
		push(@NEW,$DATA);
	}

#---------------------------------------------------------------------------------------------------
# 必須チェック
#---------------------------------------------------------------------------------------------------
	if(!open(IN,"$g_ErrFile")){ $mes = "ファイルOPENエラーです。FileName=[ $g_ErrFile ]";}
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
					$MES .= "<tr><td>[<strong class=\"caution\"> $ERR </strong>]　の項目が未入力です。</td></tr>\n";
					$mes = $MES;
				}
			}
		}
	}
	# メールアドレスチェック
	unless($MAIL=~/^[\w\-+\.]+\@[\w\-+\.]+$/i) {
		$MES .= "<tr><td>[<strong class=\"caution\"> E-mail </strong>]　の項目が間違っています。<br>正しいメールアドレスを入力してください。</td></tr>\n";
		$mes = $MES;
	}
	if($mes ne ""){
		$mes .="</table>\n";
		$mes .="<p class=\"mail-input\"><input type=\"button\" value=\"　戻　る　\" onclick=\"JavaScript:history.back();\"></p>";
		&error;
	}

	if($form{'check'} eq "" && $g_Kakunin == 1) {
#---------------------------------------------------------------------------------------------------
# 確認画面
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
		if(!open(IN,"$g_ConfirmHtmlFile")){ $mes = "ファイルOPENエラーです。FileName=[ $g_ConfirmHtmlFile ]";}
			if($mes ne ""){&error;}
			@cnfile = <IN>;
		close(IN);
		foreach $FILELINE (@cnfile){
			if($FILELINE =~ /^(.*)<!--%(\w+)%-->(.*)$/) {
				$FILELINE = "";
				$FILELINE .= "<table class=\"mail-form\" border=\"0\" cellspacing=\"1\">\n";
				$FILELINE .= $strhtml;
				$FILELINE .= "</table>\n";
				$FILELINE .= "<p class=\"mail-input\"><input type=\"button\" value=\"　戻　る　\" onclick=\"JavaScript:history.back();\">　<input type=\"button\" value=\"　送　信　\" onclick=\"document.frm.submit();\"></p>\n";
				$FILELINE .= "<form action=\"mail_table.cgi\" method=\"post\" name=\"frm\">\n" .$strvalue. "<input type=\"hidden\" name=\"check\" value=\"1\">\n</form>";
			}
			print $FILELINE;
		}
	}
	else {
#---------------------------------------------------------------------------------------------------
# メール送信
#---------------------------------------------------------------------------------------------------
		foreach $lines (@NEW){
			($A,$B) = split(/\t/,$lines);
			if($A eq "check" || $A eq "submit") {
				next;
			}
			$ML_LINE = "$A ： $B\n";
			$ML_DATA .= $ML_LINE;
		}
		if(!open(IN,"$g_ToMailFile")){$mes = 'メール用ファイルOPENエラーです。file=[ $g_ToMailFile ]';}
		if($mes ne ""){&error;}
			@m_file = <IN>;
		close(IN);
		foreach $M_FILE (@m_file){
			$M_FILE =~ s/<!--%CGI%-->/$ML_DATA/g;
			$MAILDATA .= $M_FILE;
		}
		if(!open(IN,"$g_FroMmailFile")){$mes = 'メール用ファイルOPENエラーです。file=[ $g_FroMmailFile ]';}
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
# データベース
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

		if(!open(OUT,">>$g_DataFile")){$mes = 'ファイル書きこみエラーです。FileName=[ $g_DataFile ]';}
		if($mes ne ""){&error;}
			print OUT "$NEWDATA\n";
		close(OUT);
#---------------------------------------------------------------------------------------------------
# 送信後
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
			if(!open(IN,"$g_EndHtmlFile")){ $mes = "ファイルOPENエラーです。FileName=[ $g_EndHtmlFile ]";}
				if($mes ne ""){&error;}
				@enfile = <IN>;
			close(IN);
			foreach $FILELINE (@enfile){
				if($FILELINE =~ /^(.*)<!--%(\w+)%-->(.*)$/) {
					$FILELINE = "";
					$FILELINE .= "<table class=\"mail-form\" border=\"0\" cellspacing=\"1\">\n";
					$FILELINE .= $strhtml;
					$FILELINE .= "</table>\n";
					$FILELINE .= "<p class=\"mail-input\"><input type=\"button\" value=\"　戻　る　\" onclick=\"JavaScript:location.href='$g_ReturnUrl';\"></p>\n";
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
# エラー関数
#---------------------------------------------------------------------------------------------------
sub error{
	print "Content-type:text/html\n\n";
	if(!open(IN,"$g_ErrorHtmlFile")){ print "ファイルOPENエラーです。FileName=[ $g_ErrorHtmlFile ]\n";}
		@erfile = <IN>;
	close(IN);

	foreach $ERFILES (@erfile){
		$ERFILES =~ s/<!--%CGI%-->/$mes/g;
		print $ERFILES;
	}
	exit;
}
