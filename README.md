[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MasonLS/api-monitor-saas)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MasonLS/api-monitor-saas)

# API Monitor SaaS

A simple, effective API monitoring service that helps developers track their API uptime and performance.

## Features

- 🔍 Monitor unlimited API endpoints
- ⏱️ Track response times and uptime
- 📊 Beautiful dashboard with real-time stats
- 🚨 Instant alerts when APIs go down
- 📈 Historical data and trends
- 💰 Simple, transparent pricing

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/MasonLS/api-monitor-saas.git
cd api-monitor-saas
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the monitor:
```bash
python src/monitor.py
```

4. Start the web dashboard:
```bash
python src/dashboard.py
```

Visit http://localhost:5000 to see the dashboard!

## Architecture

- **Backend**: Python with SQLite database
- **Frontend**: Flask with real-time updates
- **Monitoring**: Scheduled checks every 5 minutes
- **Alerts**: Email notifications (coming soon)

## Pricing

- **Free**: 5 monitors, 5-minute checks
- **Pro ($19/mo)**: 50 monitors, 1-minute checks, email alerts
- **Business ($49/mo)**: Unlimited monitors, 30-second checks, SMS alerts

## Roadmap

- [ ] User authentication
- [ ] Stripe payment integration
- [ ] Email/SMS alerts
- [ ] Status pages
- [ ] API access
- [ ] Multi-region monitoring
- [ ] Webhook notifications

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Email: support@apimonitor.io
- Documentation: [docs.apimonitor.io](https://docs.apimonitor.io)
- Status: [status.apimonitor.io](https://status.apimonitor.io)
