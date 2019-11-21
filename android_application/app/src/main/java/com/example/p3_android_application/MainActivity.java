package com.example.p3_android_application;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.os.*;
import android.view.View;
import android.widget.*;
import java.io.*;
import java.net.Socket;
import java.util.*;

@SuppressLint("SetTextI18n")    //This line is used to avoid IDE complaining about setText method
public class MainActivity extends Activity {

    final Handler handler = new Handler();

    private PrintWriter output;
    private BufferedReader input;

    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_value);

    }
    public void onValueButtonClick(View view){
        //start a Thread where connection to the server is made
        new Thread(new ConnectToServerThread()).start();

        //get the name of that button (e.g. "button_1")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button
        String value = String.valueOf(buttonName.charAt(buttonName.length() - 1));
        handCards = handCards + value;

        //goes to the "select suit" activity
        Intent intent = new Intent(this, ActivitySuits.class);
        startActivity(intent);
        Timer timer = new Timer(); // timer for handling the time delays and periods to send messages each 1 second
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                handler.post(new Runnable() {
                    public void run() {
                        // message sent each 1 second to the server
                        if (handCards.length() == 4)
                            new Thread(new SendMessageThread(handCards)).start();
                        else
                            new Thread(new SendMessageThread("nothing")).start();
                    }
                });
            }
        },1000,1000);
    }

    public String getHandCards() {
        return handCards;
    }

    //-----------------------------------------------------------------------------------//
        //----------------------------- CLASSES FOR THREADS -----------------------//
    //-----------------------------------------------------------------------------------//

    //used to change the intents with Thread
    class ChangeActivityThread implements Runnable {
        Class activityToChangeTo;

        ChangeActivityThread(Class activity){
            this.activityToChangeTo = activity;
        }

        public void run() {
            Intent intent = new Intent(); //to be filled
        }
    }

    class ConnectToServerThread implements Runnable {
        public void run() {
            Socket socket;
            try {
                //create a socket
                socket = new Socket("10.0.2.2", 12345);
                //create input and output streams
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // do whatever you need with the layout views immediately after connection
                    }
                });
                new Thread(new ReceiveMessageThread()).start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    class ReceiveMessageThread implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {
                    //receiving messages from the server
                    //if message is "nothing", connection renewed to continuously check for the messages
                    //if it's something else, message is sent to the CombinationChecker and RankChecker
                    final String message = input.readLine();
                    if (!message.equals("nothing")) {
                        CombinationChecker combinationChecker = new CombinationChecker(message);
                        RankChecker rankChecker = new RankChecker(message);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                //do whatever needed with the views each time the message is received
                            }
                        });
                    } else {
                        new Thread(new ConnectToServerThread()).start();
                        return;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    //this sends initially selected cards as a string
    //first char of value + first char of suit (e.g."5S")
    class SendMessageThread implements Runnable {
        private String handName;

        SendMessageThread(String handName) {
            this.handName = handName;
        }

        @Override
        public void run() {
            output.write(handName);
            output.flush();
            System.out.println("SENT THE HAND"); // for us to know when it happens
        }
    }
}

