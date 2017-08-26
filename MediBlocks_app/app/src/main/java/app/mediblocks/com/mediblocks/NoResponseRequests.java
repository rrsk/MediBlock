package app.mediblocks.com.mediblocks;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

/**
 * Created by RISHAB on 26-08-2017.
 */

public class NoResponseRequests {

    public static String global_url = "";
    public static String global_IP_Address = "http://192.168.4.29:5000/";
    static Context context;

    public static class NonResponseRequest extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... voids) {

            try{

                Log.i("flow", "doInBackground: for GetQuote ");
                String url = global_url;
                NetworkUtilities.getRequest(context,url);

            }catch( Exception e )
            {

            }
            return null;
        }

    }

    public static void addUser( String username , String email , String gender , Integer age )
    {
        global_url =global_IP_Address + "adduser?username=\""+username+"\"&email=\""+email+"\"&gender=\""+gender+"\""+"&age="+age;
        NonResponseRequest NRU = new NonResponseRequest();
        NRU.execute();
    }

    public static void addPillAndDosage( Integer user_id , String name , Integer count , Integer partition_number , String c )
    {
        global_url =global_IP_Address + "addpillanddosage?user_id="+user_id.toString()+"&minku=\""+c+"\"&name=\""+name+"\"&count="+count.toString()+"&partition_number="+partition_number.toString();
        Log.i("HITTING", global_url);
        NonResponseRequest NRU = new NonResponseRequest();
        NRU.execute();
    }

}
