package com.example.raspi;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;


import java.util.Timer;
import java.util.TimerTask;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.view.View;
import android.widget.Toast;
import android.widget.Button;

import android.content.ContentValues;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.Bundle;
import android.widget.TextView;

import org.w3c.dom.Text;

import javax.net.ssl.HttpsURLConnection;

public class HibiyaLine extends AppCompatActivity {
    private TextView emptyseats;
    String IP = "172.29.148.145";
    String PORT = "5001";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hibiya_line);

        emptyseats = (TextView) findViewById(R.id.emptyseats);
    }
    private Handler mHandler = new Handler();
    private Runnable timerTask = new Runnable() {
        @Override
        public void run() {
            String url = "http://"+IP+":"+PORT+"/api/displayEmptySeats";
            NetworkTask networkTask = new NetworkTask(url, null);
            networkTask.execute();
            mHandler.postDelayed(timerTask,3000);
        }
    };
    @Override
    public void onResume(){
        super.onResume();
        mHandler.post(timerTask);
    }
    @Override
    public void onPause(){
        super.onPause();
        mHandler.removeCallbacks(timerTask);
    }

    public class NetworkTask extends AsyncTask<Void,Void,String>{
        private String url;
        private ContentValues values;
        public  NetworkTask(String url, ContentValues values){
            this.url = url;
            this.values = values;
        }
        @Override
        protected String doInBackground(Void... voids) {
            String result;
            RequestHttpURLConnection requestHttpURLConnection = new RequestHttpURLConnection();
            result = requestHttpURLConnection.request(url, values);
            return result;
        }

        protected void onPostExecute(String s){
            super.onPostExecute(s);
            String data = "Number of empty seats in Train NO.1 => "+s.split(":")[1].replace("}","")+"seats";
            emptyseats.setText(data);
        }
    }

}
