package com.example.android_application_for_p3;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import android.view.View;


public class ActivitySetSuits extends Activity {


    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_suits);
        handCards = getIntent().getStringExtra("handCards"); // take the string from the previous activity
    }

    public void onSuitClick(View view){
        //get the name of that button (e.g. "button_1")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button
        String value = String.valueOf(buttonName.charAt(buttonName.length() - 1));
        handCards = handCards + value;

        if (handCards.length() == 4) {
            Intent intent = new Intent(this, ActivitySpeedometer.class);
            intent.putExtra("handCards", handCards);
            startActivity(intent);
        } else {
            //goes to the "select suit" activity
            Intent intent = new Intent(this, MainActivity.class);
            intent.putExtra("handCards", handCards);
            startActivity(intent);
        }
    }

    //-----------------------------------------------------------------------------------//
    //----------------------------- CLASSES FOR THREADS -----------------------//
    //-----------------------------------------------------------------------------------//

    /*class ThreadForIntent implements Runnable {
        private Intent intent;
        private int angle;
        private String combination;
        private String[] cards;

        ThreadForIntent(Intent intent, int angle, String combination, String[] cards){
            this.intent = intent;
            this.angle = angle;
            this.combination = combination;
            this.cards = cards;
        }

        @Override
        public void run() {
            intent.putExtra("angle", angle);
            intent.putExtra("combination", combination);
            intent.putExtra("cards", cards);
            startActivity(intent);
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
            } catch (IOException e) { System.out.println("Connection to the server failed"); }
        }
    }

    class ReceiveMessageThread implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {
                    //receiving messages from the server
                    //if message is "nothing", connection renewed to continuously check for the messages
                    //if it's something else, message is sent to the CombinationChecker and RankChecker and stuff done to display the info
                    final String message = input.readLine();
                    if (!message.equals("nothing")) {
                        combinationChecker = new CombinationChecker(message);
                        rankChecker = new RankChecker(message);
                        System.out.println("THIS IS AN ANGLE ----->>> " + rankChecker.getCombinationAngle());
                        System.out.println("THIS IS A RANK ----->>> " + rankChecker.getCombinationRank());
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                //do whatever needed with the views each time the message is received
                                // probably display the rank stuff and combination stuff in the views
                            }
                        });
                    } else {
                        System.out.println(message);
                        new Thread(new ConnectToServerThread()).start();
                        return;
                    }
                } catch (IOException e) { System.out.println("Receiving message failed"); }
            }
        }
    }

    //this sends initially selected cards as a String
    //first char of value + first char of suit 2x(e.g."5S7D")
    class SendMessageThread implements Runnable {
        private String handName;

        SendMessageThread(String handName) { this.handName = handName; }

        @Override
        public void run() {
            output.write(handName);
            output.flush();
            System.out.println("THE HAND IS SENT"); // for us to know when it happens
        }
    }*/
}
