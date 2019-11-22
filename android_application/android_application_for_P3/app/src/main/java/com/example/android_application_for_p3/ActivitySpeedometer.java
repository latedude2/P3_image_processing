package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Matrix;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Timer;
import java.util.TimerTask;

@SuppressLint("SetTextI18n")    //This line is used to avoid IDE complaining about setText method
public class ActivitySpeedometer extends AppCompatActivity {

    final Handler handler = new Handler(); // to handle threads to go from other threads to the main thread

    private PrintWriter output;
    private BufferedReader input;

    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)

    CombinationChecker combinationChecker;
    RankChecker rankChecker;

    ImageView speedometerView;
    TextView combinationTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_speedometer);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        speedometerView = findViewById(R.id.arrow_disk);
        combinationTextView = findViewById(R.id.combination_text);

        new Thread(new ConnectToServerThread()).start();

        handCards = getIntent().getStringExtra("handCards"); // use for taking the info to here

        Timer timer = new Timer(); // timer for handling the time delays and periods to send messages each 1 second
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                handler.post(new Runnable() {
                    public void run() {
                        // message sent each 1 second to the server
                            new Thread(new SendMessageThread(handCards)).start();
                    }
                });
            }
        }, 1000, 1000);
    }

    class ConnectToServerThread implements Runnable {
        public void run() {
            Socket socket;
            try {
                //create a socket
                socket = new Socket("192.168.43.18", 12345);
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
                    if (!message.equals("nothin")) {
                        combinationChecker = new CombinationChecker("5 2S5S6S8SJS 1800");
                        rankChecker = new RankChecker("5 2S5S6S8SJS 1800");
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                //do whatever needed with the views each time the message is received
                                // probably display the rank stuff and combination stuff in the views
                                speedometerView.setRotation(rankChecker.getCombinationAngle());
                                combinationTextView.setText(combinationChecker.getCurrentCombination());
                                for(int i = 1; i < combinationChecker.getCardAmount()+1; i++){
                                    String viewName = "card" + i;
                                    int idOfView = getResources().getIdentifier(viewName, "id", getPackageName());
                                    ImageView view = findViewById(idOfView);
                                    String cardName = combinationChecker.cardNameToViewName(i-1);
                                    int idOfImage = getResources().getIdentifier(cardName, "drawable", getPackageName());
                                    view.setImageResource(idOfImage);
                                }
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
        }
    }
}
