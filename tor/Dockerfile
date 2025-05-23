# Use Alpine Linux for minimal attack surface
FROM alpine:3.18

# Install Tor and required packages
RUN apk add --no-cache \
    tor \
    torsocks \
    # Security packages
    libcap \
    # Cleanup
    && rm -rf /var/cache/apk/*

# Create directory for hidden service
RUN mkdir -p /var/lib/tor/hidden_service && \
    chown -R tor:tor /var/lib/tor && \
    chmod 700 /var/lib/tor/hidden_service

# Copy torrc configuration
COPY torrc /etc/tor/torrc

# Set permissions
RUN chown -R tor:tor /etc/tor && \
    chmod 644 /etc/tor/torrc

# Drop capabilities but keep NET_BIND_SERVICE
RUN setcap 'cap_net_bind_service=+ep' /usr/bin/tor

# Switch to non-root user
USER tor

# Expose ports (these are internal only due to docker-compose network setup)
EXPOSE 9050
EXPOSE 80
EXPOSE 8001

# Start Tor
CMD ["tor", "-f", "/etc/tor/torrc"]

# Health check
HEALTHCHECK --interval=60s --timeout=15s --start-period=20s \
    CMD nc -z localhost 9050 || exit 1
