package com.example.raspi;

import android.content.ContentValues;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by NamHyunsil on 25/07/2019.
 */

public class RequestHttpURLConnection {
    public String request(String _url, ContentValues _params){
        HttpURLConnection urlConn = null;
        StringBuffer sbParams = new StringBuffer();
        if (_params == null)
            sbParams.append("");

        try {
            URL url = new URL(_url);
            urlConn = (HttpURLConnection) url.openConnection();

            urlConn.setRequestMethod("POST");
            urlConn.setRequestProperty("Accept-Charset", "UTF-8");
            urlConn.setRequestProperty("Context_Type", "application/x-www-form-urlencoded;charset=UTF-8");
            String strParams = sbParams.toString();
            OutputStream os = urlConn.getOutputStream();
            os.write(strParams.getBytes("UTF-8"));
            os.flush();
            os.close();

            if (urlConn.getResponseCode() != HttpURLConnection.HTTP_OK)
                return  null;
            BufferedReader reader = new BufferedReader(new InputStreamReader(urlConn.getInputStream()));

            String line;
            String page = "";
            while (((line = reader.readLine()))!=null){
                page += line;
            }
            return  page;
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            if (urlConn != null)
                urlConn.disconnect();
        }
        return  null;
    }


}