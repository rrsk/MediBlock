package app.mediblocks.com.mediblocks;

import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.GridView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Response;
import okhttp3.ResponseBody;

import static android.R.attr.value;
import static android.R.interpolator.cycle;
import static app.mediblocks.com.mediblocks.NoResponseRequests.addPillAndDosage;
import static app.mediblocks.com.mediblocks.NoResponseRequests.global_url;


public class MainActivity extends AppCompatActivity {

    static List<Pill> pills = new ArrayList<>();
    RelativeLayout RR;

    // starting @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    TextView addMed , editDose;
    FloatingActionButton fab;
    boolean optionVisibility = false;

    public void toggleOptionVisibility(View v)
    {
        optionVisibility = !optionVisibility;

        addpillFLASK addPILL = new addpillFLASK();
        addPILL.execute();

        if( optionVisibility )
        {
            addMed.setVisibility(View.VISIBLE);
            editDose.setVisibility(View.VISIBLE);
            fab.setBackgroundColor(Color.rgb(244,67,54));
        }
        else
        {
            addMed.setVisibility(View.GONE);
            editDose.setVisibility(View.GONE);
            fab.setBackgroundColor(Color.rgb(106,27,154));
        }
    }

    //ending @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    public class addpillFLASK extends AsyncTask<Void, Void, Void>{

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected Void doInBackground(Void... voids) {

            Log.i("flow", "doInBackground: for GetQuote ");
            String url = "http://www.randomtext.me/api/";
            Response res = NetworkUtilities.getRequest(getApplicationContext(),url);

            JSONObject Jobject = null;
            ResponseBody jsonData = res.body();
            try {
                Jobject = new JSONObject(jsonData.string());
            } catch (JSONException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }


            try{
                Log.i("ANS : ", "doInBackground: " + Jobject.getString("text_out"));
            } catch (Exception e)
            {

            }


            return null;
        }

        @Override
        protected void onPostExecute(Void aVoid) {
            super.onPostExecute(aVoid);
        }
    }



    public void addMedicine( View v )
    {
        Intent myIntent = new Intent(this, ADDUSER.class);
        this.startActivity(myIntent);
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        RR = (RelativeLayout) findViewById(R.id.RRR);

//        addUser("mudit" , "mudit@gmail.com" , "M" , 21 );

        NoResponseRequests.context = getApplicationContext();

        NoResponseRequests.addPillAndDosage(1,"ttttttttttttttttttttt", 10 , 3 , "010" );


        preparePillsData();

        if( MainActivity.pills.size() > 0 )
        {
            RR.setVisibility(View.GONE);
        }
        else
        {
            RR.setVisibility(View.VISIBLE);
        }

        addMed = (TextView) findViewById(R.id.addMedicine);
        editDose = (TextView) findViewById(R.id.editDosage);
        fab = (FloatingActionButton) findViewById(R.id.floating_button);
        fab.setBackgroundColor(Color.rgb(106,27,154));

        GridView gridView = (GridView) findViewById(R.id.grid);

        PillAdapter pillAdapter = new PillAdapter(this,pills);
        gridView.setAdapter(pillAdapter);


    }

    void preparePillsData(){
//        Pill pill = new Pill("Para","101");
//        pills.add(pill);
//
//        Pill pill1 = new Pill("calpol","110");
//        pills.add(pill1);
//
//        Pill pill2 = new Pill("Novaclox","001");
//        pills.add(pill2);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
