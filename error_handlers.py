from flask import render_template, request


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        app.logger.warning(f"400 - Bad Request: {e}")
        return render_template("error.html", message="Bad request."), 400

    @app.errorhandler(401)
    def unauthorized(e):
        app.logger.warning(f"401 - Unauthorized: {e}")
        return render_template("error.html", message="Unauthorized access."), 401

    @app.errorhandler(403)
    def forbidden(e):
        app.logger.warning(f"403 - Forbidden: {e}")
        return render_template("error.html", message="Permission denied."), 403

    @app.errorhandler(404)
    def not_found(e):
        app.logger.info(f"404 - Page not found: {request.url}")
        return render_template("error.html", message="Page not found."), 404

    @app.errorhandler(422)
    def unprocessable(e):
        app.logger.warning(f"422 - Unprocessable entity: {e}")
        return render_template("error.html", message="Unprocessable input."), 422

    @app.errorhandler(429)
    def too_many(e):
        app.logger.warning(f"429 - Too many requests: {e}")
        return (
            render_template(
                "error.html", message="Too many requests. Please slow down."
            ),
            429,
        )

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error("500 - Internal server error", exc_info=True)
        return render_template("error.html", message="Internal server error."), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.critical(f"Unhandled exception: {e}", exc_info=True)
        return render_template("error.html", message="Something went wrong."), 500
