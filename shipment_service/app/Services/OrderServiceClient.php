<?php
namespace App\Services;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\Log;

class OrderServiceClient
{
    protected Client $client;
    public function __construct() {
        $this->client = new Client([
            'base_uri' => env('ORDER_SERVICE_URL'), 'timeout' => 5.0, 'headers' => ['Accept' => 'application/json']
        ]);
    }
    public function getOrder(string $orderId): ?array {
        // Ambil juga user_id dari order untuk digunakan di resolver lain
        $query = 'query GetOrder($id: ID!) { order(id: $id) { id user_id status total_amount } }';
        try {
            $response = $this->client->post('', ['json' => ['query' => $query, 'variables' => ['id' => $orderId]]]);
            $data = json_decode($response->getBody()->getContents(), true);
            return $data['data']['order'] ?? null;
        } catch (\Exception $e) {
            Log::error('ShipmentService: Gagal mengambil order ' . $orderId . ': ' . $e->getMessage());
            return null;
        }
    }
    public function updateOrderStatus(string $orderId, string $status): bool {
        $mutation = 'mutation($id: ID!, $status: String!) { updateOrderStatus(id: $id, status: $status) { id status } }';
        try {
            $response = $this->client->post('', ['json' => ['query' => $mutation, 'variables' => ['id' => $orderId, 'status' => $status]]]);
            $data = json_decode($response->getBody()->getContents(), true);
            return !isset($data['errors']);
        } catch (\Exception $e) {
            Log::error('ShipmentService: Gagal update status order ' . $orderId . ': ' . $e->getMessage());
            return false;
        }
    }
}