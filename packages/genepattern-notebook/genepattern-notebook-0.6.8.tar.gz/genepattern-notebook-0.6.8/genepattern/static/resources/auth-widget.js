/**
 * Define the Jupyter GenePattern Authentication widget
 *
 * @author Thorin Tabor
 * @requires - jQuery, navigation.js
 *
 * Copyright 2015-2016 The Broad Institute, Inc.
 *
 * SOFTWARE COPYRIGHT NOTICE
 * This software and its documentation are the copyright of the Broad Institute, Inc. All rights are reserved.
 * This software is supplied without any warranty or guaranteed support whatsoever. The Broad Institute is not
 * responsible for its use, misuse, or functionality.
 */

/**
 *  Expects a list of lists with [name, url] pairs
 *  Configure this list to change what users see
 *  The top option is the default for the server
 *  Remove the 'Custom GenePattern Server' option to disallow custom servers
 */
var GENEPATTERN_SERVERS = [
    ['Broad Institute', 'https://genepattern.broadinstitute.org/gp'],
    ['Indiana University', 'https://gp.indiana.edu/gp'],
    ['GenePattern AWS Beta', 'https://gp-beta-ami.genepattern.org/gp'],
    ['Broad Internal (Broad Institute Users Only)', 'https://gpbroad.broadinstitute.org/gp'],
    ['Custom GenePattern Server', 'Custom']
];

define("genepattern/authentication", ["base/js/namespace",
                                      "nbextensions/jupyter-js-widgets/extension",
                                      "nbtools",
                                      "genepattern/navigation",
                                      "genepattern",
                                      "jqueryui"], function (Jupyter, widgets, NBToolManager, GPNotebook, gp) {

    $.widget("gp.auth", {
        options: {
            // List of GenePattern servers to appear in the menu
            servers: GENEPATTERN_SERVERS,

            // GenePattern session
            session: null,

            // Reference to the Jupyter cell
            cell: null
        },

        /**
         * Constructor
         *
         * @private
         */
        _create: function() {
            var widget = this;

            // Add data pointer
            this.element.data("widget", this);

            // Render the view.
            this.element
                .addClass("panel panel-primary gp-widget gp-widget-auth")
                .append(
                    $("<div></div>")
                        .addClass("panel-heading")
                        .append(
                            $("<div></div>")
                                .addClass("widget-float-right")
                                .append(
                                    $("<span></span>")
                                        .addClass("widget-server-label")
                                        .append(widget.getServerLabel(""))
                                )
                                .append(
                                    $("<button></button>")
                                        .addClass("btn btn-default btn-sm widget-slide-indicator")
                                        .css("padding", "2px 7px")
                                        .attr("title", "Expand or Collapse")
                                        .attr("data-toggle", "tooltip")
                                        .attr("data-placement", "bottom")
                                        .append(
                                            $("<span></span>")
                                                .addClass("fa fa-minus")
                                        )
                                        .tooltip()
                                        .click(function() {
                                            widget.expandCollapse();
                                        })
                                )
                                .append(" ")
                                .append(
                                    $("<div></div>")
                                        .addClass("btn-group")
                                        .append(
                                            $("<button></button>")
                                                .addClass("btn btn-default btn-sm")
                                                .css("padding", "2px 7px")
                                                .attr("type", "button")
                                                .attr("data-toggle", "dropdown")
                                                .attr("aria-haspopup", "true")
                                                .attr("aria-expanded", "false")
                                                .append(
                                                    $("<span></span>")
                                                        .addClass("fa fa-cog")
                                                )
                                                .append(" ")
                                                .append(
                                                    $("<span></span>")
                                                        .addClass("caret")
                                                )
                                        )
                                        .append(
                                            $("<ul></ul>")
                                                .addClass("dropdown-menu")
                                                .append(
                                                    $("<li></li>")
                                                        .append(
                                                            $("<a></a>")
                                                                .attr("title", "Toggle Code View")
                                                                .attr("href", "#")
                                                                .append("Toggle Code View")
                                                                .click(function() {
                                                                    widget.toggle_code();
                                                                })
                                                        )
                                                )
                                        )
                                )
                        )
                        .append(
                            $("<img/>")
                                .addClass("gp-widget-logo")
                                .attr("src", Jupyter.notebook.base_url + "nbextensions/genepattern/resources/" + "GP_logo_on_black.png")
                        )
                        .append(
                            $("<h3></h3>")
                                .addClass("panel-title")
                                .append(
                                    $("<span></span>")
                                        .addClass("widget-username-label")
                                        .append(widget.getUserLabel("Login"))
                                )
                        )
                    )
                .append(
                    $("<div></div>")
                        .addClass("panel-body widget-view")
                        .append(
                            $("<div></div>")
                                .addClass("gp-widget-loading")
                                .append(
                                    $("<img />")
                                        .attr("src", Jupyter.notebook.base_url + "nbextensions/genepattern/resources/" + "loader.gif")
                                )
                                .hide()
                        )
                        .append(
                            $("<div></div>")
                                .addClass("gp-widget-logged-in")
                                .append(
                                    $("<div></div>")
                                        .text("You are already logged in.")
                                        .append($("<br/>"))
                                        .append(
                                            $("<button></button>")
                                                .text("Login Again")
                                                .addClass("btn btn-warning btn-lg")
                                                .click(function() {
                                                    widget.element.find(".gp-widget-logged-in").hide();
                                                })
                                        )
                                )
                                .hide()
                        )
                        .append(
                            $("<div></div>")
                                .addClass("alert gp-widget-auth-message")
                                .hide()
                        )
                        .append(
                            $("<div></div>")
                                .addClass("gp-widget-auth-form")
                                .append(
                                    $("<div></div>")
                                        .addClass("form-group")
                                        .append(
                                            $("<label></label>")
                                                .attr("for", "server")
                                                .text("GenePattern Server")
                                        )
                                        .append(
                                            $("<select></select>")
                                                .addClass("form-control")
                                                .attr("name", "server")
                                                .attr("type", "text")
                                                .css("margin-left", "0")
                                        )
                                )
                                .append(
                                    $("<div></div>")
                                        .addClass("form-group")
                                        .append(
                                            $("<label></label>")
                                                .attr("for", "username")
                                                .text("GenePattern Username")
                                        )
                                        .append(
                                            $("<input/>")
                                                .addClass("form-control")
                                                .attr("name", "username")
                                                .attr("type", "text")
                                                .attr("placeholder", "Username")
                                                .attr("required", "required")
                                                .keyup(function (e) {
                                                    if (e.keyCode == 13) {
                                                        widget._enterPressed();
                                                    }
                                                })
                                        )
                                )
                                .append(
                                    $("<div></div>")
                                        .addClass("form-group")
                                        .append(
                                            $("<label></label>")
                                                .attr("for", "password")
                                                .text("GenePattern Password")
                                        )
                                        .append(
                                            $("<input/>")
                                                .addClass("form-control")
                                                .attr("name", "password")
                                                .attr("type", "password")
                                                .attr("placeholder", "Password")
                                                .val("")
                                                .keyup(function (e) {
                                                    if (e.keyCode == 13) {
                                                        widget._enterPressed();
                                                    }
                                                })
                                        )
                                )
                                .append(
                                    $("<button></button>")
                                        .addClass("btn btn-primary gp-auth-button")
                                        .text("Log into GenePattern")
                                        .click(function() {
                                            var server = widget.element.find("[name=server]").val();
                                            var username = widget.element.find("[name=username]").val();
                                            var password = widget.element.find("[name=password]").val();

                                            // Display the loading animation
                                            widget._displayLoading();

                                            widget.buildCode(server, username, password);
                                            widget.authenticate(server, username, password, true, function() {
                                                widget.executeCell();
                                                widget.buildCode(server, "", "");
                                                widget._tokenCountdown(server, username, password);
                                            });
                                        })
                                )
                                .append(" ")
                                .append(
                                    $("<button></button>")
                                        .addClass("btn btn-default")
                                        .text("Register an Account")
                                        .click(function() {
                                            var server = widget.element.find("[name=server]").val();
                                            var registerURL = server + "/pages/registerUser.jsf";
                                            window.open(registerURL,'_blank');
                                        })
                                )
                        )
            );

            // Add servers to select
            var serverSelect = this.element.find("[name=server]");
            $.each(this.options.servers, function(i, e) {
                var disable = GPNotebook.session_manager.get_session(e[1]) !== null;
                serverSelect.append(
                    $("<option></option>")
                        .attr("value", e[1])
                        .prop("disabled", disable)
                        .text(e[0])
                );
            });

            // If a custom URL is specified in the code, add to server dropdown
            var serverURL = widget._getCodeServerURL();
            if (serverURL !== null && widget._isURLCustom(serverURL)) {
                widget._setCustomURL(serverURL);
            }
            else {
                serverSelect.find("option[value='" + serverURL + "']").attr("selected", "selected")
            }

            // Call dialog if Custom Server selected
            serverSelect.change(function() {
                var selected = serverSelect.val();
                if (selected === "Custom") widget._selectCustomServer();
            });

            // Hide the code by default
            var element = this.element;
            var hideCode = function() {
                var cell = element.closest(".cell");
                if (cell.length > 0) {
                    element.closest(".cell").find(".input").hide();
                }
                else {
                    setTimeout(hideCode, 10);
                }
            };
            setTimeout(hideCode, 1);

            // Make calls that need run after the element has been inserted into the DOM
            setTimeout(function() {
                // Get the server URL from the code
                var server_url = widget._getCodeServerURL();

                // Grab matching session, if one is available and session is not set
                if (!widget.options.session) {
                    widget.options.session = GPNotebook.session_manager.get_session(server_url);
                }

                // Hide the login form if already authenticated and no other matching login
                var authenticated = widget.options.session !== null && widget.options.session.authenticated;
                var only_matching_login = $(".widget-server-label:contains('" + server_url + "')").length === 0;
                if (authenticated && only_matching_login) {
                    element.find(".panel-body").hide();
                    var indicator = element.find(".widget-slide-indicator").find("span");

                    // Display the logged in message
                    // widget._displayLoggedIn();

                    // Hide the login form
                    widget.hideLoginForm();

                    // Display the system message, if available
                    widget.checkSystemMessage(function() {});
                }

                // Display username and server URL in header if authenticated
                if (widget.options.session !== null && widget.options.session.authenticated) {
                    widget.element.find(".widget-username-label").text(widget.getUserLabel(""));
                    widget.element.find(".widget-server-label").text(widget.getServerLabel(""));
                }

                // Apply server color scheme if authenticated
                if (widget.options.session !== null && widget.options.session.authenticated) {
                    GPNotebook.slider.applyColors(widget.element, widget.options.session.server());
                }

                // Try reading GenePattern cookie and prompt, if cookie present and not authenticated
                var genepatternCookie = widget._getCookie("GenePattern");
                var public_server_selected = serverSelect.val() === GENEPATTERN_SERVERS[0][1];
                if (genepatternCookie && widget.options.session === null && public_server_selected) {
                    var username = widget._usernameFromCookie(genepatternCookie);
                    var password = widget._passwordFromCookie(genepatternCookie);

                    if (username !== null && password !== null) {
                        var toCover = widget.element.find(".widget-view");
                        var autoLogin = $("<div></div>")
                            .addClass("widget-auto-login")
                            .append(
                                $("<div></div>")
                                    .addClass("panel panel-default gp-cookie-login")
                                    .append(
                                        $("<div></div>")
                                            .addClass("panel-heading")
                                            .append("Log into GenePattern Server")
                                    )
                                    .append(
                                        $("<div></div>")
                                            .addClass("panel-body")
                                            .append("You have already authenticated with the GenePattern Public Server. Would you like to automatically sign in now?")
                                            .append(
                                                $("<div></div>")
                                                    .addClass("widget-auto-login-buttons")
                                                    .append(
                                                        $("<button>")
                                                            .addClass("btn btn-primary")
                                                            .append("Login as " + username)
                                                            .click(function () {
                                                                var serverInput = toCover.find("[name=server]");
                                                                var usernameInput = toCover.find("[name=username]");
                                                                var passwordInput = toCover.find("[name=password]");
                                                                var loginButton = toCover.find(".gp-auth-button");
                                                                var defaultServer = GENEPATTERN_SERVERS[0][1];

                                                                serverInput.val(defaultServer);
                                                                usernameInput.val(username);
                                                                passwordInput.val(password);
                                                                loginButton.click();
                                                            })
                                                    )
                                                    .append(" ")
                                                    .append(
                                                        $("<button>")
                                                            .addClass("btn btn-default")
                                                            .append("Cancel")
                                                            .click(function () {
                                                                autoLogin.hide();
                                                            })
                                                    )
                                            )
                                    )
                            );

                        toCover.append(autoLogin);
                    }

                }

            }, 1);

            // Trigger gp.widgetRendered event on cell element
            setTimeout(function() {
                widget.element.closest(".cell").trigger("gp.widgetRendered");
            }, 10);

            return this;
        },

        /**
         * Destructor
         *
         * @private
         */
        _destroy: function() {
            this.element.removeClass("gp-widget-job-widget");
            this.element.empty();
        },

        /**
         * Update all options
         *
         * @param options - Object contain options to update
         * @private
         */
        _setOptions: function(options) {
            this._superApply(arguments);
        },

        /**
         * Update for single options
         *
         * @param key - The name of the option
         * @param value - The new value of the option
         * @private
         */
        _setOption: function(key, value) {
            this._super(key, value);
        },

        /**
         * Set timer for next token refresh.
         * Call upon successful login.
         * Check every minute to see if the token is going to expire.
         *
         * @param server
         * @param username
         * @param password
         * @private
         */
        _tokenCountdown: function(server, username, password) {
            var widget = this;

            // Set time of successful login
            var tokenExpiration = new Date();
            tokenExpiration.setDate(tokenExpiration.getDate() + 1);

            // Wake up every minute and check to see if the token is going to expire
            setInterval(function() {
                // Refresh token five minutes before the old one would expire
                if (new Date().valueOf() >= tokenExpiration.valueOf() - 1000 * 60 * 5) {
                    widget.authenticate(server, username, password, false, function(token) {
                        tokenExpiration = new Date();
                        tokenExpiration.setDate(tokenExpiration.getDate() + 1);
                    });
                }
            }, 1000 * 60);
        },

        /**
         * Given the GenePattern cookie, returns the password
         * Return null if the password cannot be extracted
         *
         * @param cookie
         * @returns {string|null}
         * @private
         */
        _passwordFromCookie: function(cookie) {
            // Handle the null case
            if (!cookie) return null;

            // Parse the cookie
            var parts = cookie.split("|");
            if (parts.length > 1) {
                return atob(decodeURIComponent(parts[1]));
            }

            // Cookie not in the expected format
            else return null;
        },

        /**
         * Given the GenePattern cookie, returns the username
         * Return null if the username cannot be extracted
         *
         * @param cookie
         * @returns {string|null}
         * @private
         */
        _usernameFromCookie: function(cookie) {
            // Handle the null case
            if (!cookie) return null;

            // Parse the cookie
            var parts = cookie.split("|");
            if (parts.length > 1) return parts[0];

            // Cookie not in the expected format
            else return null;
        },

        /**
         * Retrieve a cookie by name
         *
         * @param name
         * @returns {string|null}
         * @private
         */
        _getCookie: function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        },

        /**
         * Prompt the user for the URL to a custom GenePattern server
         *
         * @private
         */
        _selectCustomServer: function() {
            var widget = this;
            var dialog = require('base/js/dialog');
            var urlTextBox = $("<input class='form-control gp-custom-url' type='text' value='http://127.0.0.1:8080/gp'/>");
            dialog.modal({
                notebook: Jupyter.notebook,
                keyboard_manager: Jupyter.keyboard_manager,
                title : "Enter Custom GenePattern Server URL",
                body : $("<div></div>")
                            .append("Enter the URL to your custom GenePattern server below. Please use the full URL, " +
                                    "including http:// as well as any port numbers and the trailing /gp. For example: " +
                                    "https://genepattern.broadinstitute.org/gp")
                            .append($("<br/><br/>"))
                            .append($("<label style='font-weight: bold;'>Server URL </label>"))
                            .append(urlTextBox),
                buttons : {
                    "Cancel" : {},
                    "OK" : {
                        "class" : "btn-primary",
                        "click" : function() {
                            var url = urlTextBox.val();
                            url = widget._validateCustomURL(url);
                            widget._setCustomURL(url);
                        }
                    }
                }
            });

            // Allow you to type in your URL
            urlTextBox.focus(function() { Jupyter.keyboard_manager.disable(); });
            urlTextBox.blur(function() { Jupyter.keyboard_manager.enable(); });
        },

        /**
         * Attempt to correct an incorrectly entered GenePattern URL and return the corrected version
         *
         * @param url
         * @returns {string}
         * @private
         */
        _validateCustomURL: function(url) {
            var returnURL = url;
            // Check for http:// or https://
            var protocolTest = new RegExp("(^http\:\/\/)|(https\:\/\/)");
            if (!protocolTest.test(returnURL)) returnURL = "http://" + returnURL;

            // Check for trailing slash
            var slashTest = new RegExp("\/$");
            if (slashTest.test(returnURL)) returnURL = returnURL.slice(0, -1);

            // Check for /gp
            var gpTest = new RegExp("\/gp$");
            if (!gpTest.test(returnURL)) returnURL += "/gp";

            return returnURL;
        },

        /**
         * Sets the auth widget to have the specified custom GenePattern URL
         *
         * @private
         */
        _setCustomURL: function(url) {
            var widget = this;
            var serverSelect = widget.element.find("[name=server]");

            // Add custom option
            $("<option></option>")
                .val(url)
                .text(url)
                .insertBefore(serverSelect.find("option[value=Custom]"));

            // Select the custom option
            serverSelect.val(url);
        },

        /**
         * Returns the URL specified in the backing code
         *
         * @private
         */
        _getCodeServerURL: function() {
            var code = this.options.cell.code_mirror.getValue();
            var lines = code.split("\n");
            var serverLine = null;
            lines.forEach(function(line) {
                if (line.indexOf("genepattern.register_session") >= 0) {
                    serverLine = line;
                }
            });

            // Found the line
            if (serverLine !== null) {
                var parts = serverLine.split("\"");
                return parts[1];
            }
            // Didn't find the line, return null
            else {
                return null;
            }
        },

        /**
         * Checks to see if the URLis in the server dropdown or not
         *
         * @param url
         * @private
         */
        _isURLCustom: function(url) {
            // Hack for pointing the old http URL of the public server at the new https URL
            if (url === "http://genepattern.broadinstitute.org/gp") return false;

            var widget = this;
            var serverSelect = widget.element.find("[name=server]");
            return serverSelect.find("option[value='" + url + "']").length === 0;
        },

        /**
         * Display the loading animation
         *
         * @private
         */
        _displayLoading: function() {
            this.hideMessage();
            this.element.find(".gp-widget-loading").show();
        },

        _displayLoggedIn: function() {
            this.element.find(".gp-widget-loading").hide();
            this.element.find(".gp-widget-logged-in").show();
        },

        /**
         * Hide the success or error message
         */
        hideMessage: function() {
            this.element.find(".gp-widget-auth-message").hide();
        },

        hideLoginForm: function() {
            this.element.find(".gp-widget-auth-form").hide();
        },

        /**
         * Show a success message to the user
         *
         * @param message - String containing the message to show
         */
        successMessage: function(message) {
            // Hide the loading message & logged in
            this.element.find(".gp-widget-loading").hide();
            this.element.find(".gp-widget-logged-in").hide();

            // Display the message
            const messageBox = this.element.find(".gp-widget-auth-message");
            messageBox.removeClass("alert-danger");
            messageBox.removeClass("alert-info");
            messageBox.addClass("alert-success");
            messageBox.text(message);
            messageBox.show("shake", {}, 500);
        },

        /**
         * Display an error message in the job widget
         *
         * @param message - String containing the message to show
         */
        errorMessage: function(message) {
            // Hide the loading message & logged in
            this.element.find(".gp-widget-loading").hide();
            this.element.find(".gp-widget-logged-in").hide();

            // Display the error
            const messageBox = this.element.find(".gp-widget-auth-message");
            messageBox.removeClass("alert-success");
            messageBox.removeClass("alert-info");
            messageBox.addClass("alert-danger");
            messageBox.text(message);
            messageBox.show("shake", {}, 500);
        },

        /**
         * Show an info message to the user
         *
         * @param message - String containing the message to show
         */
        infoMessage: function(message) {
            // Hide the loading message & logged in
            this.element.find(".gp-widget-loading").hide();
            this.element.find(".gp-widget-logged-in").hide();

            // Display the message
            const messageBox = this.element.find(".gp-widget-auth-message");
            messageBox.removeClass("alert-danger");
            messageBox.removeClass("alert-success");
            messageBox.addClass("alert-info");
            messageBox.html(message);
            messageBox.show();
        },

        /**
         * Click the login button if the enter key is pressed
         *
         * @private
         */
        _enterPressed: function() {
            this.element.find(".gp-auth-button").trigger("click");
        },

        expandCollapse: function() {
            var toSlide = this.element.find(".panel-body.widget-view");
            var indicator = this.element.find(".widget-slide-indicator").find("span");
            if (toSlide.is(":hidden")) {
                toSlide.slideDown();
                indicator.removeClass("fa-plus");
                indicator.addClass("fa-minus");
            }
            else {
                toSlide.slideUp();
                indicator.removeClass("fa-minus");
                indicator.addClass("fa-plus");
            }
        },

        toggle_code: function() {
            // Get the code block
            const code = this.element.closest(".cell").find(".input");
            const is_hidden = code.is(":hidden");
            const cell = this.options.cell;

            if (is_hidden) {
                // Show the code block
                code.slideDown();
                GPNotebook.slider.set_metadata(cell, "show_code", true);
            }
            else {
                // Hide the code block
                code.slideUp();
                GPNotebook.slider.set_metadata(cell, "show_code", false);
            }
        },

        buildCode: function(server, username, password) {
            var cell = this.options.cell;
            GPNotebook.init.buildCode(cell, server, username, password);
        },

        executeCell: function() {
            this.options.cell.execute();
        },

        /**
         * Call the authentication endpoint, then call afterAuthenticate() if set
         *
         * @param server
         * @param username
         * @param password
         * @param callAfterAuthenticate
         * @param done
         */
        authenticate: function(server, username, password, callAfterAuthenticate, done) {
            var widget = this;
            $.ajax({
                type: "POST",
                url: server + "/rest/v1/oauth2/token?grant_type=password&username=" + encodeURIComponent(username) +
                        "&password=" + encodeURIComponent(password) + "&client_id=GenePatternNotebook-" + encodeURIComponent(username),
                cache: false,
                xhrFields: {
                    withCredentials: true
                },
                success: function(data) {
                    var token = data['access_token'];

                    // Register the session
                    var session = GPNotebook.session_manager.register_session(server, username, password);
                    widget.options.session = session;
                    session.token = token;

                    if (callAfterAuthenticate) widget.afterAuthenticate(server, username, password, token, done);
                    else done(token);
                },
                error: function() {
                    widget.buildCode(server, "", "");
                    widget.errorMessage("Error authenticating");
                }
            });
        },

        /**
         * Assumes the authenticate endpoint has already been called,
         * then does all the other stuff needed for authentication
         *
         * @param server
         * @param username
         * @param password
         * @param token
         * @param done
         */
        afterAuthenticate: function(server, username, password, token, done) {
            var widget = this;
            $.ajax({
                type: "GET",
                url: server + "/rest/v1/tasks/all.json",
                dataType: 'json',
                cache: false,
                headers: {"Authorization": "Bearer " + token},
                xhrFields: {
                    withCredentials: true
                },
                success: function(data) {
                    // Set the authentication info on GenePattern object
                    widget.options.session.authenticated = true;
                    widget.options.session.server(server);
                    widget.options.session.username = username;
                    widget.options.session.password = password;
                    widget.options.session.token = token;

                    // Make authenticated UI changes to auth widget
                    widget.element.find(".widget-username-label").text(username);
                    widget.element.find(".widget-server-label").text(server);

                    // Enable authenticated nav elsewhere in notebook
                    GPNotebook.slider.authenticate(widget.options.session, data);

                    // Populate the GenePattern._tasks list
                    if (data['all_modules']) {
                        $.each(data['all_modules'], function(index, module) {
                            widget.options.session._tasks.push(new widget.options.session.Task(module));
                        });
                    }

                    // Populate the GenePattern._kinds map
                    var kindMap = widget.options.session.linkKinds(data['kindToModules']);
                    GPNotebook.slider.removeKindVisualizers(kindMap);
                    widget.options.session.kinds(kindMap);

                    // If a function to execute when done has been passed in, execute it
                    if (done) { done(token); }
                },
                error: function() {
                    widget.errorMessage("Error loading server info");
                }
            });
        },

        /**
         * Returns a node with a feedback message and button, to be appended to the system message
         *
         * @param feedbackLink
         * @returns {*|jQuery|HTMLElement}
         */
        createFeedbackMessage: function(feedbackLink) {
            return $("<div></div>")
                .addClass("clearfix")
                .css("padding-top", "10px")
                .append(
                    $("<button></button>")
                        .addClass("btn btn-primary btn-lg pull-right")
                        .css("margin-left", "10px")
                        .text("Leave Feedback")
                        .click(function() {
                            window.open(feedbackLink, '_blank');
                            // window.location.href = feedbackLink;
                        })
                )
                .append(
                    $("<p></p>")
                        .addClass("lead")
                        .text("Experiencing a bug? Have thoughts on how to make GenePattern Notebook better? Let us know by leaving feedback.")
                )
        },

        /**
         * Checks the system message and displays the message, if one is found
         * Calls the done() method regardless of success or error
         *
         * @param done
         */
        checkSystemMessage: function(done) {
            var widget = this;
            $.ajax({
                type: "GET",
                url: widget.options.session.server() + "/rest/v1/config/system-message",
                dataType: 'html',
                cache: false,
                headers: {"Authorization": "Bearer " + widget.options.session.token},
                xhrFields: {
                    withCredentials: true
                },
                success: function(data) {
                    // Display if the system message is not blank
                    if (data !== "") {
                        // Strip data of HTML
                        var cleanMessage = $("<div></div>").html(data).text().trim();

                        var messageBlock = $("<div></div>");

                        // If there is a message
                        if (cleanMessage !== "") {
                            messageBlock.append(
                                $("<div></div>")
                                    .text(cleanMessage)
                            );
                            messageBlock.append("<hr/>");
                        }

                        // Append the feedback message
                        messageBlock.append(
                            widget.createFeedbackMessage("http://software.broadinstitute.org/cancer/software/genepattern/contact")
                        );

                        // Display the system message
                        widget.infoMessage(messageBlock);
                    }

                    // If a function to execute when done has been passed in, execute it
                    if (done) { done(); }
                },
                error: function() {
                    // Assume that the server is not a version that supports the system message call

                    // Attach the feedback messafe
                    var message = widget.createFeedbackMessage("http://software.broadinstitute.org/cancer/software/genepattern/contact");
                    widget.infoMessage(message);

                    // If a function to execute when done has been passed in, execute it
                    if (done) { done(); }
                }
            });
        },

        getUserLabel: function(alt) {
            if (this.options.session !== null && this.options.session.authenticated && this.options.session.username) {
                return this.options.session.username;
            }
            else {
                return alt
            }
        },

        getServerLabel: function(alt) {
            if (this.options.session !== null && this.options.session.authenticated && this.options.session.server()) {
                return this.options.session.server();
            }
            else {
                return alt
            }
        }
    });

    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Shift-d', {
        help : 'toggle dev servers',
        help_index : 'ee',
        handler : function () {
            GPNotebook.slider.toggleDev();
            return false;
        }}
    );

    // Method to enable dev servers from the auth widget
    GPNotebook.slider.toggleDev = function() {
        function addOptions() {
            $(".gp-widget-auth-form").find("[name=server]").each(function(i, select) {
                $(select)
                    .addClass("gp-widget-dev-on")
                    .append(
                        $("<option></option>")
                            .val("http://genepatternbeta.broadinstitute.org/gp")
                            .text("gpbeta")
                    )
                    .append(
                        $("<option></option>")
                            .val("http://gpdev.broadinstitute.org/gp")
                            .text("gpdev")
                    )
                    .append(
                        $("<option></option>")
                            .val("http://127.0.0.1:8080/gp")
                            .text("localhost")
                    )
            });
        }

        function removeOptions() {
            $(".gp-widget-auth-form").find("[name=server]").each(function(i, select) {
                $(select).removeClass("gp-widget-dev-on");
                $(select).find("option[value='http://genepatternbeta.broadinstitute.org/gp']").remove();
                $(select).find("option[value='http://gpdev.broadinstitute.org/gp']").remove();
                $(select).find("option[value='http://127.0.0.1:8080/gp']").remove();
            });
        }

        // Toggle
        var devOn = $(".gp-widget-auth-form").find("[name=server]").hasClass("gp-widget-dev-on");
        var devWord = devOn ? "off" : "on";
        if (devOn) removeOptions();
        else addOptions();

        // Show dialog
        var dialog = require('base/js/dialog');
        dialog.modal({
            notebook: Jupyter.notebook,
            keyboard_manager: this.keyboard_manager,
            title : "Development Options Toggled",
            body : "You have toggled development options " + devWord + " for GenePattern Notebook.",
            buttons : {
                "OK" : {}
            }
        });
    };

    var AuthWidgetView = widgets.DOMWidgetView.extend({
        render: function () {
            let cell = this.options.cell;

            // Ugly hack for getting the Cell object in ipywidgets 7
            if (!cell) cell = this.options.output.element.closest(".cell").data("cell");

            // Protect against double-rendering
            if (cell.element.find(".gp-widget").length > 0) return;

            // Check to see if this auth widget was manually created, if so replace with full code
            if (!('genepattern' in cell.metadata) && cell.code_mirror.getValue().trim() !== "") {
                GPNotebook.init.buildCode(cell, GENEPATTERN_SERVERS[0][1], "", "");
            }

            // Render the view.
            if (!this.el) this.setElement($('<div></div>'));

            $(this.$el).auth({
                cell: cell
            });

            // Hide the code by default
            var element = this.$el;
            setTimeout(function() {
                // Protect against the "double render" bug in Jupyter 3.2.1
                element.parent().find(".gp-widget-auth:not(:first-child)").remove();

                element.closest(".cell").find(".input").hide();
            }, 1);
        }
    });

    var AuthWidgetTool = new NBToolManager.NBTool({
        origin: "+",
        id: "authentication",
        name: "GenePattern Login",
        // tags: ["GenePattern", "Authentication"],
        description: "Sign into a GenePattern Server",
        load: function() { return true; },
        render: function() {
            var cell = Jupyter.notebook.get_selected_cell();
            var is_empty = cell.get_text().trim() == "";

            // If this cell is not empty, insert a new cell and use that
            // Otherwise just use this cell
            if (!is_empty) {
                cell = Jupyter.notebook.insert_cell_below();
                Jupyter.notebook.select_next();
            }

            GPNotebook.slider.createAuthCell(cell);
            return cell;
        }
    });

    return {
        AuthWidgetView: AuthWidgetView,
        AuthWidgetTool: AuthWidgetTool
    }
});