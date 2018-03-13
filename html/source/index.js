import lc from "laconic";
import qrcode from "qrcode-generator-es6";

let email = JSON.parse(localStorage.getItem("email"));
let email_e = document.getElementById("email");

const update_email = () => {
  if (!email) {
    email_e.textContent = "Guest";
  } else {
    email_e.textContent = email;
  }
  localStorage.setItem("email", JSON.stringify(email));
};

const clear_email = () => {
  email = null;
  update_email();
};

const change_email = ({doAfter}) => {
  const text = lc.input({
    type: "email",
    placeholder: "your-address@example.com"
  });
  const change = lc.button(
    {
      type: "submit"
    },
    "Change"
  );
  const cancel = lc.button(
    {
      type: "submit"
    },
    "Cancel"
  );
  const popup = lc.div(
    {
      id: "popup"
    },
    lc.div(
      lc.h5("Change Email"),
      lc.p("Download links for purchased assets are sent to this address."),
      text,
      lc.div(
        {
          class: "buttons"
        },
        change,
        cancel
      )
    )
  );
  const close = () => {
    popup.parentNode.removeChild(popup);
  };
  change.addEventListener("click", () => {
    email = text.value;
    update_email();
    close();
    if (doAfter) {
      doAfter();
    }
  });
  cancel.addEventListener("click", () => {
    close();
  });
  document.getElementsByTagName("body")[0].appendChild(popup);
};

const show_address = e => {
  const addressMount = lc.div();
  const close = lc.button(
    {
      type: "submit",
      onclick: () => {
        popup.parentNode.removeChild(popup);
      }
    },
    "Close"
  );
  const popup = lc.div(
    {
      id: "popup"
    },
    lc.div(
      lc.p(
        "Purchase via ",
        lc.a(
          {
            href: "https://micromicro.cash"
          },
          "micromicro"
        )
      ),
      addressMount,
      lc.div(
        {
          class: "buttons"
        },
        close
      )
    )
  );
  document.getElementsByTagName("body")[0].appendChild(popup);
  fetch("CREATE ADDRESS URL", {
    method: "POST",
    body: JSON.stringify({
      email: email,
      id: e.value
    })
  })
    .then(r => r.text())
    .then(r => {
      const uri = "https://micromicro.cash/app/index.html#in/" + r;
      const qr = new qrcode(0, "H");
      qr.addData(uri);
      qr.make();
      var parser = new DOMParser();
      var address = parser.parseFromString(
        qr.createSvgTag({
          margin: 0
        }),
        "application/xml"
      ).firstElementChild;
      const link = lc.a(
        {
          href: uri
        },
        address
      );
      addressMount.parentNode.replaceChild(link, addressMount);
    })
    .catch(e => {
      console.log(e);
    });
};

update_email();

document.getElementById("change_email").onclick = change_email;

document.getElementById("clear_email").onclick = clear_email;

Array.prototype.forEach.call(document.getElementsByTagName("data"), e => {
  const button = lc.button(
    {
      onclick: () => {
        if (!email) {
          change_email({
            doAfter: () => show_address(e)
          });
        } else {
          show_address(e);
        }
      }
    },
    "Buy"
  );
  e.appendChild(button);
});
