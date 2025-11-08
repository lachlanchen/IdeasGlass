import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

class IdeasGlassTelemetryEvent {
  IdeasGlassTelemetryEvent({
    required this.deviceId,
    required this.timestamp,
    this.battery,
    this.ambientLux,
    this.micLevel,
    this.photo,
  });

  final String deviceId;
  final DateTime timestamp;
  final int? battery;
  final double? ambientLux;
  final double? micLevel;
  final Map<String, dynamic>? photo;

  factory IdeasGlassTelemetryEvent.fromJson(Map<String, dynamic> json) {
    return IdeasGlassTelemetryEvent(
      deviceId: json['device_id'] as String,
      timestamp:
          DateTime.fromMillisecondsSinceEpoch((json['ts'] as num) * 1000, isUtc: true),
      battery: (json['battery'] as num?)?.toInt(),
      ambientLux: (json['ambient_lux'] as num?)?.toDouble(),
      micLevel: (json['mic_level'] as num?)?.toDouble(),
      photo: json['photo'] as Map<String, dynamic>?,
    );
  }
}

class IdeasGlassSyncService {
  IdeasGlassSyncService({
    required this.baseUrl,
    required this.deviceId,
    required this.deviceSecret,
    http.Client? httpClient,
  }) : _http = httpClient ?? http.Client();

  final Uri baseUrl;
  final String deviceId;
  final String deviceSecret;
  final http.Client _http;

  WebSocketChannel? _channel;
  StreamController<IdeasGlassTelemetryEvent>? _controller;

  Stream<IdeasGlassTelemetryEvent> get deviceStream {
    _controller ??= StreamController<IdeasGlassTelemetryEvent>.broadcast(
      onListen: _maybeOpenSocket,
      onCancel: _handleCancel,
    );
    return _controller!.stream;
  }

  Uri get _ingestUri => baseUrl.resolve('/api/v1/ingest');

  Future<void> publishTelemetry(Map<String, dynamic> payload) async {
    final body = jsonEncode({
      'device_id': deviceId,
      ...payload,
    });

    final response = await _http.post(
      _ingestUri,
      headers: {
        'Content-Type': 'application/json',
        'X-Device-Secret': deviceSecret,
      },
      body: body,
    );

    if (response.statusCode >= 400) {
      throw Exception('IdeasGlass ingest failed: ${response.statusCode} -> ${response.body}');
    }
  }

  void _maybeOpenSocket() {
    if (_channel != null) return;
    final wsScheme = baseUrl.scheme == 'https' ? 'wss' : 'ws';
    final wsUri = Uri(
      scheme: wsScheme,
      host: baseUrl.host,
      port: baseUrl.hasPort ? baseUrl.port : null,
      path: '/ws/devices/$deviceId',
    );
    _channel = WebSocketChannel.connect(wsUri);
    _channel!.stream.listen(
      _handleSocketMessage,
      onError: (error) {
        debugPrint('IdeasGlass ws error: $error');
        _reconnect();
      },
      onDone: _reconnect,
    );
  }

  void _handleSocketMessage(dynamic raw) {
    if (_controller == null || raw == null) return;
    final data = jsonDecode(raw as String) as Map<String, dynamic>;
    if (data['type'] != 'telemetry') return;
    final payload = data['payload'] as Map<String, dynamic>;
    _controller!.add(IdeasGlassTelemetryEvent.fromJson(payload));
  }

  void _reconnect() {
    _channel?.sink.close();
    _channel = null;
    if (_controller?.hasListener ?? false) {
      Future<void>.delayed(const Duration(seconds: 2), _maybeOpenSocket);
    }
  }

  void _handleCancel() {
    _channel?.sink.close();
    _channel = null;
    _controller?.close();
    _controller = null;
  }

  void dispose() {
    _handleCancel();
    _http.close();
  }
}
