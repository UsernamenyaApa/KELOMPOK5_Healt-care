<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('shipment_updates', function (Blueprint $table) {
            $table->id();
            $table->foreignId('shipment_id')->constrained()->onDelete('cascade'); // Relasi ke tabel shipments
            $table->string('status'); // Status pada update ini
            $table->text('location')->nullable();
            $table->text('description')->nullable();
            $table->timestamps(); // Timestamp untuk kapan update ini terjadi
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('shipment_updates');
    }
};
