package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.*;
import android.os.*;
import android.view.View;
import android.widget.*;

import java.io.*;
import java.net.Socket;
import java.util.*;

@SuppressLint("SetTextI18n")    //This line is used to avoid IDE complaining about setText method
public class ActivitySpeedometer extends AppCompatActivity {
    // to handle threads to go from other threads to the main thread
    final Handler handler = new Handler();

    //input and output to communicate to the server
    private PrintWriter output;
    private BufferedReader input;

    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)

    // used to decrypt the string sent from server
    CombinationChecker combinationChecker; // gives the combination and cards to display
    RankChecker rankChecker; // gives an angle of how much the speedometer should be rotated

    ImageView speedometerView;
    TextView combinationTextView;

    boolean roundIsOn; // used to control the threads, so when the round needs to repeat, all threads should be killed

    int modeLength = 3;
    String[] readCombinations = {" ", " ", " "}; //used to store the current combination before taking mode
    int[] calculatedAngles = new int[modeLength]; //used to find mode of angles
    int modeIndex = 0;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_speedometer);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());
        roundIsOn = true;

        speedometerView = findViewById(R.id.arrow_disk);
        combinationTextView = findViewById(R.id.combination_text);

        // connect to the server
        new Thread(new ConnectToServerThread()).start();

        handCards = getIntent().getStringExtra("handCards"); // use for taking the info to here

        Timer timer = new Timer(); // timer for handling the time delays and periods to send messages each 1 second
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                handler.post(new Runnable() {
                    public void run() {
                        // message sent each 1 second to the server if the round is still on
                        if (roundIsOn) {
                            new Thread(new SendMessageThread()).start();
                        }
                    }
                });
            }
        }, 1000, 1000);
    }

    // when the "next round" button is clicked
    public void onNextRoundClick(View view){
        roundIsOn = false; //destroys all of the threads
        new Thread(new NextRoundThread(this)).start(); // creates new thread to start a new round
    }

    //---------------------------------------------------------------------------//
        //---------------------- CLASSES FOR THREADS ----------------------//
    // --------------------------------------------------------------------------//

    class NextRoundThread implements Runnable {
        Context context;
        NextRoundThread(Context context){ this.context = context; }
        @Override
        public void run() {
            startActivity(new Intent(context, ActivityCardInput.class));
        }
    }

    class ConnectToServerThread implements Runnable {
        public void run() {
            if (roundIsOn) {
                Socket socket;
                try {
                    //create a socket
                    socket = new Socket("172.20.10.4", 12345);
                    //create input and output streams
                    output = new PrintWriter(socket.getOutputStream());
                    input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    new Thread(new ReceiveMessageThread()).start();
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            // do whatever you need with the layout views immediately after connection
                            // probably not needed
                        }
                    });
                } catch (IOException e) { System.out.println("Connection to the server failed"); }
            }
        }
    }

    class ReceiveMessageThread implements Runnable {
        @Override
        public void run() {
            while (roundIsOn) {
                try {
                    //receiving messages from the server
                    //if message is "nothing", thread is repeated to continuously check for the messages
                    //if it's something else, message is sent to the CombinationChecker and RankChecker and stuff done to display the info
                    String message = input.readLine();
                    if (!message.equals("nothing")) {
                        combinationChecker = new CombinationChecker(message); //check what is the combination and the cards to display
                        rankChecker = new RankChecker(message); //check what is the the angle that the speedometer should be turned around
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                //do whatever needed with the views each time the message is received
                                // that should be displaying the rank, combination name and cards in the views
                                calculatedAngles[modeIndex] = rankChecker.getCombinationAngle();
                                readCombinations[modeIndex] = combinationChecker.getCurrentCombination();

                                if (modeIndex < modeLength - 1){
                                    modeIndex++;
                                }
                                else { modeIndex = 0; }
                                System.out.println("index = " + modeIndex);

                                speedometerView.setRotation(findMode(calculatedAngles)); // rotate the speedometer
                                combinationTextView.setText(findMode(readCombinations)); // set combination text

                                for(int i = 1; i < combinationChecker.getCardAmount()+1; i++){
                                    // take the card id (from 1 up to 5) make id from it and take the needed view
                                    ImageView view = findViewById(
                                            getResources().getIdentifier("card" + i,
                                                    "id",
                                                    getPackageName()));
                                    //display the image of the card
                                    view.setImageResource(
                                            getResources().getIdentifier(
                                                    combinationChecker.cardNameToViewName(i-1),
                                                    "drawable",
                                                    getPackageName()));
                                }
                            }
                        });
                    } else {
                        // if message was "nothing", then try to receive thread again
                        new Thread(new ReceiveMessageThread()).start();
                        return;
                    }
                } catch (IOException e) { System.out.println("Receiving message failed"); }
            }
        }
    }

    static int findMode(int[] list){
        int mode = list[0];

        //finding the the mode of the combinations
        int maxCounter = 0; //used to store the amount of cards in current mode
        for (int i = 0; i < list.length; i++){ //checking though the stored combinations
            int counter = 0; // to count repetitions of current combination

            // circling through all saved combinations counting the matches
            for (int j = 0; j < list.length; j++){
                if (list[i] == list[j] && list[i] != 0){
                    System.out.println("got here");
                    counter++;
                }
            }
            //Checking if the combination we just counted beats the current mode
            if (counter >= maxCounter){
                maxCounter = counter;
                //saving the mode
                mode = list[i];
            }
        }
        System.out.println("angle mode = " + mode);
        return mode;
    }

    static String findMode (String[] list){
        String mode = list[0];


        //finding the the mode of the combinations
        int maxCounter = 0; //used to store the amount of cards in current mode
        for (int i = 0; i < list.length; i++){ //checking though the stored combinations
            int counter = 0; // to count repetitions of current combination

            // circling through all saved combinations counting the matches
            for (int j = 0; j < list.length; j++){
                if (!list[i].equals(" ") && list[i].equals(list[j])){
                    counter++;
                }
            }
            //Checking if the combination we just counted beats the current mode
            if (counter >= maxCounter){
                maxCounter = counter;
                //saving the mode
                mode = list[i];
            }
        }
        System.out.println("combination mode = " + mode);
        return mode;
    }


    //this sends initially selected cards as a String
    //first char of value + first char of suit 2x(e.g."5S7D")
    class SendMessageThread implements Runnable {
        @Override
        public void run() {
            if (roundIsOn) {
                output.write(handCards);
                output.flush();
            }
        }
    }
}
