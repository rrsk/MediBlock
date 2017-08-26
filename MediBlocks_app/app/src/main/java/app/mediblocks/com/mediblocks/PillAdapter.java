package app.mediblocks.com.mediblocks;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import java.util.List;

/**
 * Created by RISHAB on 25-08-2017.
 */

public class PillAdapter extends BaseAdapter {

    private final Context mContext;
    private final List<Pill> pills;


    public PillAdapter(Context context, List<Pill> pills) {
        this.mContext = context;
        this.pills =pills;
    }

    @Override
    public int getCount() {
        return pills.size();
    }

    // 3
    @Override
    public long getItemId(int position) {
        return 0;
    }

    // 4
    @Override
    public Object getItem(int position) {
        return null;
    }

    // 5
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        final Pill pill = pills.get(position);

        if(convertView == null){
            final LayoutInflater layoutInflater = LayoutInflater.from(mContext);
            convertView = layoutInflater.inflate(R.layout.pill_card,null);

        }

        final ImageView pillPic = (ImageView)convertView.findViewById(R.id.pill_pic);

        final TextView pillName = (TextView)convertView.findViewById(R.id.pill_name);

        final TextView pillCount = (TextView)convertView.findViewById(R.id.pill_count);

        TextView pillDosage = (TextView)convertView.findViewById(R.id.pill_dosage);

        if(position == 0){
            pillPic.setImageResource(R.drawable.pill1);
        }
        else if(position == 1){
            pillPic.setImageResource(R.drawable.pill2);
        }
        else if(position == 2){
            pillPic.setImageResource(R.drawable.pill3);
        }
        else{
            pillPic.setImageResource(R.drawable.pill4);
        }

        pillName.setText("Name : " + pill.getName());

        pillDosage.setText("Dosage : " + pill.getDosage());

        pillCount.setText("Count : " + Integer.toString(pill.getCount()));

        return convertView;
    }
}
