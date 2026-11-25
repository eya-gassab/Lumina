package com.eyagassab.lumina.sync;

import android.content.Context;

import androidx.work.BackoffPolicy;
import androidx.work.Constraints;
import androidx.work.ExistingPeriodicWorkPolicy;
import androidx.work.NetworkType;
import androidx.work.PeriodicWorkRequest;
import androidx.work.WorkManager;

import java.util.concurrent.TimeUnit;

public final class SyncScheduler {

    public static final String DAILY_SYNC_WORK_NAME = "lumina_daily_sync_work";

    private SyncScheduler() {
        // Classe utilitaire
    }

    public static void scheduleDailySync(Context context) {
        Constraints constraints = new Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build();

        PeriodicWorkRequest syncRequest = new PeriodicWorkRequest.Builder(
                DailySyncWorker.class,
                24, TimeUnit.HOURS
        )
                .setConstraints(constraints)
                .setBackoffCriteria(
                        BackoffPolicy.EXPONENTIAL,
                        PeriodicWorkRequest.MIN_BACKOFF_MILLIS,
                        TimeUnit.MILLISECONDS
                )
                .build();

        // KEEP évite de dupliquer ou de réinitialiser la tâche si elle est déjà planifiée
        WorkManager.getInstance(context.getApplicationContext()).enqueueUniquePeriodicWork(
                DAILY_SYNC_WORK_NAME,
                ExistingPeriodicWorkPolicy.KEEP,
                syncRequest
        );
    }
}