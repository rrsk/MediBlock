package app.mediblocks.com.mediblocks;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import static app.mediblocks.com.mediblocks.MainActivity.pills;

public class ADDUSER extends AppCompatActivity {

    EditText name , number , section;
    CheckBox morning , afternoon , evening ;
    TextView errorTV;
    Boolean error = false;

    public void showErrorMsg()
    {
        if( error )
        {
            errorTV.setVisibility(View.VISIBLE);
        }
        else
        {
            errorTV.setVisibility(View.GONE);
        }
        error = false;
    }

    public boolean check( String str )
    {
        if( str == null )
        {
            return true;
        }
        else if( str == "" )
        {
            return true;
        }
        return false;
    }

    public void addUserSubmit(View v)
    {
        String username=null , count=null , section_local=null ;

        boolean nameB , numberB , sectionB ;
        nameB = check(name.getText().toString());
        numberB = check(number.getText().toString());
        sectionB = check(section.getText().toString());

        String dosage = "";

        if( sectionB || nameB || numberB  )
        {
            error = true;
            showErrorMsg();
            return ;
        }

        if( !morning.isChecked() && !afternoon.isChecked() && !evening.isChecked() )
        {
            error = true;
            showErrorMsg();
            return ;
        }

        if( morning.isChecked() )
        {
            dosage = dosage + "1";
        }
        else
        {
            dosage = dosage + "0";
        }

        if( afternoon.isChecked() )
        {
            dosage = dosage + "1";
        }
        else
        {
            dosage = dosage + "0";
        }

        if( evening.isChecked() )
        {
            dosage = dosage + "1";
        }
        else
        {
            dosage = dosage + "0";
        }

        username = name.getText().toString();
        count = number.getText().toString();
        section_local = section.getText().toString();

        NoResponseRequests.addPillAndDosage(3,username, Integer.parseInt(count), Integer.parseInt(section_local) , dosage);

        Pill pill = new Pill(username,dosage,Integer.parseInt(count));
        MainActivity.pills.add(pill);

        Intent myIntent = new Intent(this, MainActivity.class);
        this.startActivity(myIntent);

    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_adduser);

        name = (EditText) findViewById(R.id.pillnameET);
        number = (EditText) findViewById(R.id.pillcountET);
        section = (EditText) findViewById(R.id.pillpartitionET);
        morning = (CheckBox) findViewById(R.id.morning);
        afternoon = (CheckBox) findViewById(R.id.afternoon);
        evening = (CheckBox) findViewById(R.id.evening);
        errorTV = (TextView) findViewById(R.id.error);
    }
}
