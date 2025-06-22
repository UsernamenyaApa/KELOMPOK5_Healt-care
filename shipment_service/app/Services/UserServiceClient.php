<?php
namespace App\Services;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\Log;

class UserServiceClient
{
    protected Client $client;
    public function __construct() {
        $this->client = new Client([
            'base_uri' => env('USER_SERVICE_URL'), 'timeout' => 5.0, 'headers' => ['Accept' => 'application/json']
        ]);
    }
    public function getUser(string $userId): ?array {
        // Ambil juga alamat untuk pengiriman
        $query = 'query GetUser($id: ID!) { user(id: $id) { id name email addresses { street city zip_code } } }';
        try {
            $response = $this->client->post('', ['json' => ['query' => $query, 'variables' => ['id' => $userId]]]);
            $data = json_decode($response->getBody()->getContents(), true);
            return $data['data']['user'] ?? null;
        } catch (\Exception $e) {
            Log::error('ShipmentService: Gagal mengambil user ' . $userId . ': ' . $e->getMessage());
            return null;
        }
    }
}