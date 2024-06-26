const message = (type, message) => {

    let toast = $("<div style='letter-spacing: 1.8px; width: 26rem;'></div>").addClass(`text-wrap fw-bold alert alert-${type}`).html(message);

    $("#toast-container").append(toast);

    setTimeout(() => {
        toast.fadeOut();
    }, 5000);
};