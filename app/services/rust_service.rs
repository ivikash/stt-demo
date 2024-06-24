use crate::core::webrtc_rust::WebRTCServer;

pub struct RustService {
    webrtc_server: WebRTCServer,
}

impl RustService {
    pub fn new() -> Self {
        RustService {
            webrtc_server: WebRTCServer::new(),
        }
    }

    pub fn start(&mut self) {
        self.webrtc_server.run();
    }
}
