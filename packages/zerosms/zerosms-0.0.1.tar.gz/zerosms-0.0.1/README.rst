zerosms
==============
Send a text message via Way2SMS to your friends and family in India. Enter your India mobile number and sms text message as parameters. Your Free SMS sending to India will be delivered instantly
----


Description: zerosms
        ==============
                
        It is python package to Send a text message via "Way2SMS"
        Send a text message to your friends and family in India. Enter your India mobile number and sms text message as parameters. Your Free SMS sending to India will be delivered instantly


        Requirements
        ============================
        BeautifulSoup4
        requests
        urllib3 1.22
        

        NOTE
        ============================

        
        use Way2Sms site credentials to send sms and future message

        ----
        
        Example Code
        ------------
        
        Open Python Interpreter::
        
            >>> import zerosms
            >>> zerosms.sms(phno=phonenum,passwd=password,message='helloworld!!',receivernum=receiver mobile number)

            >>> zerosms.futuresms(phno=phno,passwd=password,set_time='17:47',set_date='15/12/2017',receivernum=receiver mobile num,message='helloworld!!')

        