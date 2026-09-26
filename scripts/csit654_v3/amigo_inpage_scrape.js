/**
 * In-page Amigo quiz scraper for CSIT654.
 * Paste/run via CDP Runtime.evaluate on an amigo.amityonline.com page.
 * Returns JSON for one cmid, or batch for cmids array.
 */
async function scrapeOne(cmid, {finish = true} = {}) {
  const abs = (u) => new URL(u, location.origin).href;
  const get = async (url) => {
    const r = await fetch(abs(url), {credentials: 'include'});
    const html = await r.text();
    return {url: r.url, html, status: r.status};
  };
  const postForm = async (action, fields) => {
    const body = new URLSearchParams(fields);
    const r = await fetch(abs(action), {
      method: 'POST',
      credentials: 'include',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body,
      redirect: 'follow',
    });
    const html = await r.text();
    return {url: r.url, html, status: r.status};
  };
  const parseDom = (html) => {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    return doc;
  };
  const extractQs = (doc) => {
    return [...doc.querySelectorAll('.que')].map((q) => {
      const stem = (q.querySelector('.qtext')?.innerText || '').trim();
      const opts = [...q.querySelectorAll('.answer > div')]
        .map((d) => (d.innerText || '').replace(/\s+/g, ' ').trim())
        .filter((t) => t && !/^Clear/i.test(t));
      const right = (q.querySelector('.rightanswer')?.innerText || '').trim();
      const state = (q.querySelector('.state')?.innerText || '').trim();
      let correct = null;
      [...q.querySelectorAll('.answer > div')].forEach((d, i) => {
        if (d.classList.contains('correct')) correct = i;
      });
      if (correct == null && /Correct/i.test(state)) {
        const checked = q.querySelector('input[type=radio]:checked');
        if (checked) correct = parseInt(checked.value, 10);
      }
      if (correct == null && right) {
        const norm = right
          .replace(/^The correct answer is:?\s*/i, '')
          .replace(/^[a-d][.)]\s*/i, '')
          .trim()
          .toLowerCase();
        opts.forEach((o, i) => {
          const on = o.replace(/^[a-d][.)]\s*/i, '').trim().toLowerCase();
          if (on === norm || on.includes(norm) || norm.includes(on)) correct = i;
        });
      }
      return {
        no: (q.querySelector('.qno')?.innerText || '').trim(),
        stem,
        options: opts,
        correct,
        correctOptionText: right || null,
        state,
        answerSource: correct != null ? 'amigo_review' : null,
        explanation: right
          ? `Amigo review: ${right.replace(/^The correct answer is:?\s*/i, '')}`
          : '',
      };
    });
  };

  // 1) view page
  let view = await get(`/mod/quiz/view.php?id=${cmid}`);
  let doc = parseDom(view.html);
  const sesskey =
    doc.querySelector('input[name=sesskey]')?.value ||
    (view.html.match(/sesskey=([a-zA-Z0-9]+)/) || [])[1];

  // Already on review?
  const reviewLink = [...doc.querySelectorAll('a')].find((a) =>
    /review\.php\?attempt=/i.test(a.getAttribute('href') || '')
  );
  if (reviewLink) {
    const rev = await get(reviewLink.getAttribute('href'));
    const qs = extractQs(parseDom(rev.html));
    return {cmid, status: 'scraped', from: 'existing_review', questions: qs, url: rev.url};
  }

  // Continue or start
  const cont = [...doc.querySelectorAll('a, button')].find((el) =>
    /Continue your attempt|Re-attempt|Attempt quiz|Start attempt/i.test(el.textContent || '')
  );
  // Prefer form startattempt
  let attemptHtml = null;
  let attemptUrl = null;
  const startForm = [...doc.querySelectorAll('form')].find((f) =>
    /startattempt/i.test(f.getAttribute('action') || '')
  );
  if (startForm) {
    const fields = {};
    startForm.querySelectorAll('input').forEach((inp) => {
      if (inp.name) fields[inp.name] = inp.value;
    });
    const res = await postForm(startForm.getAttribute('action'), fields);
    attemptHtml = res.html;
    attemptUrl = res.url;
  } else {
    // continue link
    const contA = [...doc.querySelectorAll('a')].find((a) =>
      /attempt\.php\?attempt=/i.test(a.getAttribute('href') || '')
    );
    if (contA) {
      const res = await get(contA.getAttribute('href'));
      attemptHtml = res.html;
      attemptUrl = res.url;
    } else {
      // button forms often post to startattempt.php
      const btnForm = [...doc.querySelectorAll('form')].find((f) =>
        /attempt|continue/i.test(f.innerText)
      );
      if (btnForm) {
        const fields = {};
        btnForm.querySelectorAll('input').forEach((inp) => {
          if (inp.name) fields[inp.name] = inp.value;
        });
        const res = await postForm(btnForm.getAttribute('action') || location.href, fields);
        attemptHtml = res.html;
        attemptUrl = res.url;
      }
    }
  }

  if (!attemptHtml) {
    return {
      cmid,
      status: 'blocked',
      note: 'No attempt/continue/start form found',
      questions: [],
    };
  }

  doc = parseDom(attemptHtml);
  // If already review
  if (/review\.php/i.test(attemptUrl) || doc.querySelector('.rightanswer')) {
    return {
      cmid,
      status: 'scraped',
      from: 'attempt_landed_review',
      questions: extractQs(doc),
      url: attemptUrl,
    };
  }

  // Extract mid-attempt (backup)
  let midQs = extractQs(doc);
  if (!finish) {
    return {cmid, status: 'scraped', from: 'mid_attempt', questions: midQs, url: attemptUrl};
  }

  // Finish: submit responseform with next=Finish
  const form = doc.querySelector('#responseform') || doc.querySelector('form');
  if (!form) {
    return {cmid, status: 'partial', note: 'no responseform', questions: midQs, url: attemptUrl};
  }
  const fields = {};
  form.querySelectorAll('input, select, textarea').forEach((inp) => {
    if (!inp.name) return;
    if (inp.type === 'radio' || inp.type === 'checkbox') {
      if (inp.checked) fields[inp.name] = inp.value;
      return;
    }
    fields[inp.name] = inp.value;
  });
  // answer first option for each unanswered so Moodle accepts
  form.querySelectorAll('.que').forEach((q) => {
    const radios = [...q.querySelectorAll('input[type=radio]')].filter(
      (r) => r.value !== '-1' && r.name
    );
    if (!radios.length) return;
    if (!radios.some((r) => r.checked)) {
      fields[radios[0].name] = radios[0].value;
    }
  });
  fields['next'] = 'Finish attempt ...';
  fields['timeup'] = fields['timeup'] || '0';

  let sum = await postForm(form.getAttribute('action'), fields);
  let sumDoc = parseDom(sum.html);

  // summary -> submit all and finish
  const finishForm = [...sumDoc.querySelectorAll('form')].find((f) =>
    /Submit all and finish|finishattempt/i.test(f.innerHTML + (f.getAttribute('action') || ''))
  );
  if (finishForm || /summary\.php/i.test(sum.url)) {
    const ffields = {};
    const ff =
      finishForm ||
      [...sumDoc.querySelectorAll('form')].find((f) =>
        f.querySelector('button, input[type=submit]')
      );
    if (ff) {
      ff.querySelectorAll('input').forEach((inp) => {
        if (inp.name) ffields[inp.name] = inp.value;
      });
      // Moodle often needs finishattempts=1
      const submitBtn = [...ff.querySelectorAll('button, input')].find((b) =>
        /Submit all and finish/i.test(b.value || b.textContent || '')
      );
      if (submitBtn && submitBtn.name) ffields[submitBtn.name] = submitBtn.value || '1';
      ffields['finishattempt'] = '1';
      if (sesskey) ffields['sesskey'] = sesskey;
      sum = await postForm(ff.getAttribute('action') || sum.url, ffields);
      sumDoc = parseDom(sum.html);
    }
  }

  // confirmation page
  if (/Submit all and finish|Confirmation/i.test(sumDoc.body?.innerText || '')) {
    const confForm = sumDoc.querySelector('form');
    if (confForm) {
      const cfields = {};
      confForm.querySelectorAll('input').forEach((inp) => {
        if (inp.name) cfields[inp.name] = inp.value;
      });
      const yes = [...confForm.querySelectorAll('button, input')].find((b) =>
        /Submit all and finish|Yes/i.test(b.value || b.textContent || '')
      );
      if (yes && yes.name) cfields[yes.name] = yes.value || '1';
      sum = await postForm(confForm.getAttribute('action') || sum.url, cfields);
      sumDoc = parseDom(sum.html);
    }
  }

  let qs = extractQs(sumDoc);
  if (!qs.length || qs.every((q) => q.correct == null)) {
    // try follow review link
    const revA = [...sumDoc.querySelectorAll('a')].find((a) =>
      /review\.php\?attempt=/i.test(a.getAttribute('href') || '')
    );
    if (revA) {
      const rev = await get(revA.getAttribute('href'));
      qs = extractQs(parseDom(rev.html));
      return {cmid, status: 'scraped', from: 'review_link', questions: qs, url: rev.url};
    }
  }
  return {
    cmid,
    status: qs.length ? 'scraped' : 'empty',
    from: 'finish_flow',
    questions: qs.length ? qs : midQs,
    url: sum.url,
  };
}

// expose
window.__csit654ScrapeOne = scrapeOne;
window.__csit654ScrapeBatch = async (cmids) => {
  const out = [];
  for (const id of cmids) {
    try {
      out.push(await scrapeOne(String(id)));
    } catch (e) {
      out.push({cmid: String(id), status: 'error', note: String(e), questions: []});
    }
  }
  return out;
};
'ready';
