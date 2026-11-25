package com.eyagassab.lumina;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.viewpager2.widget.ViewPager2;

import com.eyagassab.lumina.data.ConceptRepository;
import com.eyagassab.lumina.ui.feed.CardAdapter;
import com.eyagassab.lumina.ui.feed.ScalePageTransformer;

import java.util.Collections;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private final ExecutorService syncExecutor = Executors.newSingleThreadExecutor();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        CardAdapter adapter = new CardAdapter(Collections.emptyList());
        ViewPager2 viewPager = findViewById(R.id.viewPager);
        viewPager.setAdapter(adapter);
        viewPager.setPageTransformer(new ScalePageTransformer());

        ConceptRepository repository = new ConceptRepository(this);
        repository.observeConcepts().observe(this, adapter::setConcepts);

        // Synchronisation initiale en arrière-plan (jamais sur le Main Thread)
        syncExecutor.execute(repository::syncDailyConceptsBlocking);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        syncExecutor.shutdown();
    }
}