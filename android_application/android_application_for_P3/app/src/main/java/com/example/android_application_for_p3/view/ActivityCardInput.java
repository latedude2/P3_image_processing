package com.example.android_application_for_p3.view;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.*;

import com.example.android_application_for_p3.R;

public class ActivityCardInput extends AppCompatActivity {

    ImageButton confirmButton;
    String handCards = "";
    String cards = "";
    String card1 = "";
    String card2 = "";
    String cardIndex = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_card_input);
        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        confirmButton = findViewById(R.id.confirm_button);
        confirmButton.setVisibility(View.GONE);

        if (getIntent().getStringExtra("cards") != null){
            Intent intentBefore = getIntent();
            cards = intentBefore.getStringExtra("cards"); // takes the name of currently chosen card
            cardIndex = intentBefore.getStringExtra("cardIndex"); // takes the card, which should be changed
            if (cardIndex != null) {
                if (cardIndex.equals("1")){ // checks if that card is on the left
                    //card1 = cards; // if yes, card on the left takes the name of the chosen card
                    card2 = intentBefore.getStringExtra("card2"); // card's on the right value is taken
                    // if card on the right is not empty it displays the card which was there before
                    if (card2 != null && !card2.equals("")) displayCard("2", card2);
                    if(cards.equals(card2)){
                        displayCard(cardIndex, "card_back");
                        Toast.makeText(this, "Incorrect choice. Try again", Toast.LENGTH_LONG).show();
                    } else {
                        card1 = cards;
                        displayCard(cardIndex, card1); // the card which was now chosen is displayed
                        handCards = card1 + card2; // handCards is updated
                    }

                    // kind of explained but from the other card above ^^^^^^^^^^^^
                } else if (cardIndex.equals("2")){
                    card1 = intentBefore.getStringExtra("card1");
                    if (card1 != null && !card1.equals("")) displayCard("1", card1);
                    if (cards.equals(card1)){
                        displayCard(cardIndex, "card_back");
                        Toast.makeText(this, "Incorrect choice. Try again", Toast.LENGTH_LONG).show();
                    } else {
                        card2 = cards;
                        displayCard(cardIndex, card2);
                        handCards = card1 + card2;
                    }

                }
            }
        }
        if (handCards.length() == 4){
            confirmButton.setVisibility(View.VISIBLE);
        }
    }

    void displayCard(String cardIndex, String card){
        //take the view by it's name and index
        ImageView imageView = findViewById(
                getResources().getIdentifier("card" + cardIndex, "id", getPackageName()));
        //display the given card image
        imageView.setImageResource(
                getResources().getIdentifier(card, "drawable", getPackageName()));
    }

    public void onCardClick(View view){
        Intent intent = new Intent(this, ActivitySetSuits.class);
        String viewName = getResources().getResourceName(view.getId());
        cardIndex = String.valueOf(viewName.charAt(viewName.length()-1));
        //sending to the other activity
        intent.putExtra("cardIndex", cardIndex); // card index, which was chosen by the user
        intent.putExtra("card1", card1); // info about card on the left
        intent.putExtra("card2", card2); // info about card on the right
        startActivity(intent); // go to the next activity
    }

    public void onConfirmClick(View view){
        Intent intent = new Intent(this, ActivitySpeedometer.class);
        intent.putExtra("handCards", handCards); // send the hand card to the speedometer activity
        startActivity(intent);
    }
}